# default-TEM-model
AxonDeepSeg default TEM model and testing image. This model is suited for a resolution of 0.01 micrometer per pixel and was trained on mouse brain data collected via a Transmission Electron Microscope (TEM).


# Steps to train this model
1. Get `ivadomed` version: [[55fc2067]](https://github.com/ivadomed/ivadomed/commit/55fc2067cbb9c97a711e32cf8b5a377fb6d517be)
2. Get the data: `data_axondeepseg_tem` (Dataset Annex version: c778a33323a6e6c9c5bf38bd1e8a7038686f3423)
3. Copy the "model_seg_mouse_axon-myelin_tem.json" file and update the following fields: `path_output`, `path_data` and `gpu_ids`.
4. Run ivadomed: `ivadomed -c path/to/the/config/file`
5. The trained model file will be saved under the `path_output` directory.
