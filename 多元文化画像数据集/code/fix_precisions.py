"""修复 model.pkl 中 GMM 的 precisions_cholesky_ 形状错误。
diag 协方差类型下, precisions_cholesky_ 应为 (n_components, n_features) = 1/sqrt(var),
而非 (n_components, n_features, n_features) 的 cholesky 矩阵。
"""
import os, pickle
import numpy as np

RES = '/Users/f.fantasiachopin/Documents/code/Research/Test20260822/多元文化画像数据集/result'
pkl = os.path.join(RES, 'model.pkl')

with open(pkl, 'rb') as f:
    bundle = pickle.load(f)

gmm = bundle['gmm']
print('covariance_type:', gmm.covariance_type)
print('covariances_ shape:', gmm.covariances_.shape)
print('precisions_cholesky_ shape (修复前):', gmm.precisions_cholesky_.shape)

# diag 协方差: precisions_cholesky_ = 1 / sqrt(var), shape (n_components, n_features)
gmm.precisions_cholesky_ = 1.0 / np.sqrt(gmm.covariances_)
print('precisions_cholesky_ shape (修复后):', gmm.precisions_cholesky_.shape)

# 同时确保 precisions_ 一致性(供可能的查询)
gmm.precisions_ = 1.0 / gmm.covariances_

with open(pkl, 'wb') as f:
    pickle.dump(bundle, f)
print('已保存修复后的 model.pkl')

# 验证 predict 可用
X = np.random.default_rng(0).normal(size=(5, gmm.n_features_in_))
probs = gmm.predict_proba(X)
labels = gmm.predict(X)
print('predict 验证通过, labels:', labels)
print('precisions_cholesky_ 前2行:', gmm.precisions_cholesky_[:2])
