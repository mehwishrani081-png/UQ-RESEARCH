"""LIDC-IDRI adapter using pylidc only; no XML parsing or filename matching."""
from __future__ import annotations
from pathlib import Path
import numpy as np
from .common import CommonSample, SampleMeta
from .splits import patient_split

def _scanner_manufacturer(scan):
    try:
        import pydicom
        files = sorted(Path(scan.get_path_to_dicom_files()).glob("*"))
        for path in files:
            if path.is_file():
                ds = pydicom.dcmread(str(path), stop_before_pixels=True, force=True)
                value = getattr(ds, "Manufacturer", None)
                if value:
                    return str(value).strip()
    except Exception as exc:
        raise LIDCDataError(f"Could not read scanner Manufacturer for {scan.patient_id}: {exc}") from exc
    raise LIDCDataError(f"Scanner Manufacturer missing for {scan.patient_id}")

class LIDCDataError(RuntimeError):
    pass

def _import_pylidc():
    try:
        import pylidc as pl
    except ImportError as exc:
        raise LIDCDataError("pylidc is required for LIDC ingestion") from exc
    return pl

def _resample2d(array, current_spacing, target_spacing, order):
    from skimage.transform import resize
    sy, sx = map(float, current_spacing)
    ty = tx = float(target_spacing)
    out_shape = (max(1, int(round(array.shape[0] * sy / ty))),
                 max(1, int(round(array.shape[1] * sx / tx))))
    out = resize(array, out_shape, order=order, preserve_range=True,
                 anti_aliasing=(order == 1))
    return out.astype(np.float32 if order == 1 else np.uint8)

def _crop_center(image, masks, cy, cx, h, w):
    y0, x0 = int(round(cy))-h//2, int(round(cx))-w//2
    y1, x1 = y0+h, x0+w
    py0, px0 = max(0,-y0), max(0,-x0)
    py1, px1 = max(0,y1-image.shape[0]), max(0,x1-image.shape[1])
    ys, ye, xs, xe = max(0,y0), min(image.shape[0],y1), max(0,x0), min(image.shape[1],x1)
    ic, mc = image[ys:ye,xs:xe], masks[:,ys:ye,xs:xe]
    if py0 or py1 or px0 or px1:
        ic = np.pad(ic,((py0,py1),(px0,px1)),mode="edge")
        mc = np.pad(mc,((0,0),(py0,py1),(px0,px1)),mode="constant")
    if ic.shape != (h,w):
        raise LIDCDataError("LIDC crop failed")
    return ic.astype(np.float32), mc.astype(np.uint8)

def _full_mask(annotation, volume_shape):
    mask = np.zeros(volume_shape, dtype=np.uint8)
    bbox = annotation.bbox()
    mask[bbox] = annotation.boolean_mask().astype(np.uint8)
    return mask

def build_lidc_samples(root, *, target_spacing_mm=.7, hu_low=-1000,
                       hu_high=400, crop_size=(128,128), seed=20261003):
    pl = _import_pylidc()
    root = Path(root).expanduser().resolve()
    if not root.exists():
        raise LIDCDataError(f"Genuine LIDC root does not exist: {root}")
    scans = pl.query(pl.Scan).all()
    if not scans:
        raise LIDCDataError("pylidc returned zero scans; refusing fallback")
    patients = sorted({s.patient_id for s in scans})
    splits = patient_split(patients, seed=seed)
    patient_to_split = {p:k for k,ids in splits.items() for p in ids}
    samples = []
    for scan in scans:
        groups = scan.cluster_annotations(verbose=False)
        if not groups:
            continue
        volume = np.asarray(scan.to_volume(verbose=False), dtype=np.float32)
        if volume.ndim != 3 or volume.shape[2] == 0:
            raise LIDCDataError(f"Invalid volume: {scan.patient_id}")
        for ni, group in enumerate(groups):
            if len(group) > 4:
                print(f"FLAG_MANUAL_INSPECTION patient={scan.patient_id} nodule={ni} annotations={len(group)}")
                raise LIDCDataError("Cluster has >4 annotations; manual inspection required")
            masks = np.stack([_full_mask(a, volume.shape) for a in group], axis=0)
            if masks.shape[0] < 4:
                masks = np.concatenate([masks, np.zeros((4-masks.shape[0],)+masks.shape[1:],dtype=np.uint8)])
            image_rs = np.stack([_resample2d(volume[:,:,z],scan.pixel_spacing,target_spacing_mm,1)
                                 for z in range(volume.shape[2])],axis=0)
            mask_rs = np.stack([
                np.stack([_resample2d(masks[r,:,:,z],scan.pixel_spacing,target_spacing_mm,0)
                          for z in range(volume.shape[2])],axis=0)
                for r in range(4)
            ],axis=0)
            union = np.any(mask_rs.astype(bool),axis=0)
            areas = union.reshape(union.shape[0],-1).sum(axis=1)
            positive = np.flatnonzero(areas>0)
            if not len(positive):
                raise LIDCDataError(f"No positive slice after resampling: {scan.patient_id}/{ni}")
            selected = positive if patient_to_split[scan.patient_id]=="TRAIN" else [int(positive[np.argmax(areas[positive])])]
            for z in selected:
                im = np.clip(image_rs[z],hu_low,hu_high)
                im = ((im-hu_low)/(hu_high-hu_low)).astype(np.float32)
                mm = mask_rs[:,:,z].astype(np.uint8)
                coords=np.argwhere(np.any(mm.astype(bool),axis=0))
                cy,cx=coords.mean(axis=0)
                im,mm=_crop_center(im,mm,cy,cx,*crop_size)
                marked=int(np.any(mm.astype(bool),axis=(1,2)).sum())
                samples.append(CommonSample(im,mm,SampleMeta(
                    scan.patient_id,f"{scan.patient_id}-nodule-{ni}-slice-{int(z)}",
                    4,marked,_scanner_manufacturer(scan),
                    (float(target_spacing_mm),float(target_spacing_mm)))))
    return samples, splits
