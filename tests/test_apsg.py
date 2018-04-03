#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Tests for `apsg` module.
"""


import pytest
import numpy as np


from apsg import *


def test_lin2vec2lin():
    assert Vec3(Lin(110, 37)).aslin == Lin(110, 37)


def test_fol2vec2fol():
    assert Vec3(Fol(213, 52)).asfol == Fol(213, 52)


def test_rotation_rdegree():
    g = Group.randn_lin()
    assert np.allclose(g.rotate(Lin(45, 45), 90).rdegree, g.rdegree)


def test_rotation_angle_lin():
    l1, l2 = Group.randn_lin(2)
    D = DefGrad.from_axis(Lin(45, 45), 60)
    assert np.allclose(l1.angle(l2), l1.transform(D).angle(l2.transform(D)))


def test_rotation_angle_fol():
    f1, f2 = Group.randn_fol(2)
    D = DefGrad.from_axis(Lin(45, 45), 60)
    assert np.allclose(f1.angle(f2), f1.transform(D).angle(f2.transform(D)))


def test_resultant_rdegree():
    g = Group.from_array([45, 135, 225, 315], [45, 45, 45, 45], Lin)
    c1 = g.R.uv == Lin(0, 90)
    c2 = np.allclose(abs(g.R), np.sqrt(8))
    c3 = np.allclose((g.rdegree/100 + 1)**2, 2)
    assert c1 and c2 and c3


def test_cross_product():
    l1 = Lin(110, 22)
    l2 = Lin(163, 47)
    p = l1**l2
    assert np.allclose(p.angle(l1), p.angle(l2), 90)


def test_axial_addition():
    l1, l2 = Group.randn_lin(2)
    assert l1.transform(l1.H(l2)) == l2


def test_vec_H():
    m = Lin(135, 10) + Lin(315, 10)
    assert m.uv == Lin(135, 0)


def test_ortensor_orthogonal():
    f = Group.randn_fol(1)[0]
    assert np.allclose(*Ortensor(Group([f.V, f.rake(-45), f.rake(45)])).eigenvals)


def test_group_heterogenous_error():
    with pytest.raises(Exception) as exc:
        g = Group([Fol(10, 10), Lin(20, 20)])
        assert "All data in group must be of same type." == str(exc.exception)


def test_group_heterogenous_error():
    with pytest.raises(Exception) as exc:
        g = Group([1, 2, 3])
        assert "Data must be Fol, Lin or Vec3 type." ==  str(exc.exception)


def test_pair_misfit():
    n, l = Group.randn_lin(2)
    f = n.asfol
    p = Pair.from_pair(f, f - l.proj(f))
    assert np.allclose(p.misfit, 0)


def test_pair_rotate():
    n, l = Group.randn_lin(2)
    f = n.asfol
    p = Pair.from_pair(f, f - l.proj(f))
    pr = p.rotate(Lin(45, 45), 120)
    assert np.allclose(p.fvec.angle(p.lvec), pr.fvec.angle(pr.lvec), 90)


def test_lin_vector_dd():
    l = Lin(120, 30)
    assert Lin(*l.V.dd) == l


def test_fol_vector_dd():
    f = Fol(120, 30)
    assert Lin(*f.V.dd).asfol == f


def test_fault_rotation_sense():
    f = Fault(90, 30, 110, 28, -1)
    assert repr(f.rotate(Lin(220, 10), 60)) == 'F:343/37-301/29 +'
