import tensorflow as tf
import ncrmodel
# print("entered maaaqaapppppp")
tf.enable_eager_execution()
param_dir = "C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\ncr_hpo_params\\params"
word_model_file = "C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\ncr_hpo_params\\params\\pmc_model_new.bin"
model = ncrmodel.NCR.loadfromfile(param_dir, word_model_file)

print(model.get_match('retina cancer', 2))