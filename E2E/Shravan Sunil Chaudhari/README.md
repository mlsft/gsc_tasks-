CV: http://bit.ly/Shravan_S_Chaudhari-CV 

Github: https://github.com/Shra1-25

# Cern_HSF_tasks
## Running inference on python:
This repository contains 9 files including this Readme file.  
SingleElectronPt50_IMGCROPS_n249k_RHv1_inference.hdf5 and SinglePhotonPt50_IMGCROPS_n249k_RHv1_inference.hdf5 are the subsets of the larger datasets on which the model was trained. The larger datasets can be accessed here:  
https://cernbox.cern.ch/index.php/s/AtBT8y4MiQYFcgc (photons)  
https://cernbox.cern.ch/index.php/s/FbXw3V4XNyYB3oA (electrons)
You can go through the model training notebook which is Keras_CERN.ipynb. This model was trained and developed using Keras 2.1.5 (The version of keras had to be downgraded in order to make it compatible with the Cern CMSSW framework.). model1.hdf5 stores the weights of the trained model and model1.json has the architecture of the trained model.  
pytorch1.pt is the model trained using pytorch. The training notebook for the same is Pytorch_CERN.ipynb.  
You may run the keras_inference.py script for the inference of model trained by Keras_CERN.ipynb. The keras version required is atleast 2.1.5 for this too. Ensure that model1.hdf5, model1.json, SingleElectronPt50_IMGCROPS_n249k_RHv1_inference.hdf5 and SinglePhotonPt50_IMGCROPS_n249k_RHv1_inference.hdf5 files are in same directory for successful execution of the keras_inference.py script.

## Running inference on CMSSW framework (using non-standalone images) with docker:
After starting the interactive shell of Docker type the following command:  
1) docker run --rm --cap-add SYS_ADMIN --device /dev/fuse -it clelange/cc7-cmssw-cvmfs /bin/bash  
(This may take few minutes to download and mount Fuse.)  
The output might look like the following:  
![GitHub Logo](/CMSSW_images/img1.png)
  
2) cmsrel CMSSW_11_0_1  
(This may take few minutes.)  
The output might look like the following:  
![GitHub Logo](/CMSSW_images/img2.png)
  
3) cd CMSSW_11_0_1/src  
4) cmsenv  
(This may take few minutes.)  
The output might look like the following:  
![GitHub Logo](/CMSSW_images/img3.png)
  
5) git clone https://github.com/Shra1-25/Cern_HSF_tasks.git  
The output might look like the following:  
![GitHub Logo](/CMSSW_images/img4.png)
6) cd Cern_HSF_tasks  
7) scram b  
The output might look like the following:  
![GitHub Logo](/CMSSW_images/img5.png)
8) python keras_inference.py  (Alternatively you can use cmsRun keras_inference.py)  
(This might take few minutes while executing for the first time. After first execution the rest of the executions will not take much time.)  
The script will ask the user to input batch size. The output might look like the following:  
Using python keras_inference.py-  
![GitHub Logo](/CMSSW_images/img6.png)  
  
Using cmsRun keras_inference.py-  
![GitHub Logo](/CMSSW_images/img7.png)  
## Inference  
The ROC curve of the model is shown at the last cell of the Keras training notebook(Keras_CERN.ipynb).  
The ROC AUC score of the model on the validation dataset is 0.796.  
The ROC curve of the model on validation dataset is as follows:  
![GitHub Logo](/CMSSW_images/img8.png)  
You may view the above figure in the Keras_CERN.ipynb notebook too (last cell of the notebook).  
The trained models have training accuracy of around 73% and validation accuracy of around 72%.  
The inference script takes as input the following files: SingleElectronPt50_IMGCROPS_n249k_RHv1_inference.hdf5 and SinglePhotonPt50_IMGCROPS_n249k_RHv1_inference.hdf5 which are subsets of the original datasets as mentioned above. The script takes as input the batch size from user. The script will then randomly select the batch of the entered batch size from the input files, run the model on the batch and save the output in outputs.csv file alongwith displaying the predictions of first 20 samples and their ground truth values (i.e. true values).  
The repository will be updated periodically after finetuning the model for improvising the accuracy.  


