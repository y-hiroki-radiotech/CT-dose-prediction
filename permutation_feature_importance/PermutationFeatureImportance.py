from __future__ import annotations
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Any, Union, Callable, List
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_squared_log_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt
import japanize_matplotlib


@dataclass
class PermutationFeatureImportance:
    """Permutation Feature Importance (PFI)
    
    Args:
        estimator: 全特徴量を用いた学習済みモデル
        X: 特徴量
        y: 目的変数
        var_names: 特徴量の名前
        eval_func: 予測精度の評価関数
    """
    estimator: Any
    X: Union[pd.DataFrame, np.ndarray]
    y: Union[pd.DataFrame, np.ndarray]
    var_names: list[str]
    eval_func: Callable[[np.ndarray, np.ndarray], float]
    
    def __post_init__(self) -> None:
        """シャッフルなしの場合の予測精度を計算する"""
        self.baseline = self.eval_func(
            self.y, self.estimator.predict(self.X)
        )
        
    def _permutation_metrics(self, idx_to_permute: int) -> float:
        """ある特徴量の値をシャッフルした時の予測精度を求める
        
        Args:
            idx_to_permute: シャッフルする特徴量のインデックス
        """
        
        X_permuted = self.X.copy()
        
        # 特徴量の値をシャッフルして予測
        if isinstance(self.X, pd.DataFrame):
            X_permuted = self.X.copy()
            X_permuted.iloc[:, idx_to_permute] = np.random.permutation(X_permuted.iloc[:, idx_to_permute])
        else:  # np.ndarray
            X_permuted = self.X.copy()
            X_permuted[:, idx_to_permute] = np.random.permutation(X_permuted[:, idx_to_permute])

        y_pred = self.estimator.predict(X_permuted)
        
        return self.eval_func(self.y, y_pred)
    
    def permutation_feature_importance(self, n_shuffle: int=10) -> None:
        """PFIを求める
        
        Args:
            n_shuffle: シャッフルの回数。デフォルトは10回
        """
        J = self.X.shape[1] # 特徴量の数
        
        # J個の特徴量に対してPFIを求める
        # R回シャッフルを繰り返して平均を取ることで値を安定させる
        metrics_permuted = [
            np.mean([self._permutation_metrics(j) for r in range(n_shuffle)]) for j in range(J)
        ]
        
        # データフレームとしてまとめる
        # シャッフルしてどのくらい予測精度が落ちるかは,
        #　差と比率の2種類を用意する
        df_feature_importance = pd.DataFrame(
            data={
                "var_name": self.var_names,
                "baseline": self.baseline,
                "permutation": metrics_permuted,
                "difference": metrics_permuted - self.baseline,
                "ratio": metrics_permuted / self.baseline,
            }
        )
        
        self.feature_importance = df_feature_importance.sort_values("permutation", ascending=False)
        
        
    def plot(self, importance_type: str = 'difference') -> None:
        """PFIを可視化
        
        Args:
            importance_type: PFIを差(difference)と比率(ratio)のどちらで計算するか
        """
        fig, ax = plt.subplots()
        ax.barh(
            self.feature_importance['var_name'],
            self.feature_importance[importance_type],
            label=f'baseline: {self.baseline:.2f}'
        )
        ax.set(xlabel=importance_type, ylabel=None)
        ax.invert_yaxis()
        ax.legend(loc='lower right')
        fig.suptitle(f'Permutationによる特徴量の重要度({importance_type})')
        
        fig.show()