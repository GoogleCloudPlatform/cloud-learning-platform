"""contains metrics"""
import tensorflow as tf
from services.dataset import Dataset
class BinaryAccuracy(tf.keras.metrics.BinaryAccuracy):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)


class AUC(tf.keras.metrics.AUC):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)


class Precision(tf.keras.metrics.Precision):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)


class Recall(tf.keras.metrics.Recall):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)


class SensitivityAtSpecificity(tf.keras.metrics.SensitivityAtSpecificity):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)


class SpecificityAtSensitivity(tf.keras.metrics.SpecificityAtSensitivity):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)


class FalseNegatives(tf.keras.metrics.FalseNegatives):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)


class FalsePositives(tf.keras.metrics.FalsePositives):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)


class TrueNegatives(tf.keras.metrics.TrueNegatives):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)


class TruePositives(tf.keras.metrics.TruePositives):
  def update_state(self, y_true, y_pred, sample_weight=None):
    true, pred = Dataset.get_target(y_true, y_pred)
    super().update_state(y_true=true,y_pred=pred,
    sample_weight=sample_weight)
