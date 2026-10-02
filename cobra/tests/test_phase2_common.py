"""Phase-2 invariant tests.
CONTROLLED FIXTURE — NOT A SCIENTIFIC RESULT.
"""
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from data.common import CommonSample,SampleMeta,validate_common_sample
from data.splits import patient_split,assert_disjoint

def test_mask_stack():
    image=np.zeros((8,8),dtype=np.float32)
    masks=np.zeros((3,8,8),dtype=np.uint8); masks[1,2:4,2:4]=1
    validate_common_sample(CommonSample(image,masks,SampleMeta("p1","s1",3,1,"test",(0.7,0.7))))

def test_no_patient_leak():
    splits=patient_split([f"p{i}" for i in range(20)],seed=7); assert_disjoint(splits)

def test_agreement_sets_nested():
    masks=np.zeros((3,4,4),dtype=np.uint8)
    masks[0,:3,:3]=1; masks[1,:2,:3]=1; masks[2,:1,:2]=1
    agreement=masks.mean(0); previous=None
    for q in np.linspace(.01,1.0,100):
        level=agreement>=q
        if previous is not None: assert np.all(level<=previous)
        previous=level
