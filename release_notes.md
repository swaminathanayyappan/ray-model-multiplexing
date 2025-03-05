# Model multiplexing serve app

This is an automated release of model multiplexing ray serve application that uses text translation model (English to French) from hugging face transformers library.

The model is available in three variants:
- t5-small
- t5-base
- t5-large

These models will have it's own weights which are different among one other, this release demonstrates how a model multiplexing serve application deployment can be automated and deployed into a AKS cluster which is installed with KubeRay , a custom resource definition (CRD) used for running Ray based workloads.

## Asset files

This release will contains the asset files which is compressed and used to deploy the app into the KubeRay cluster, the application code will present in app/ directory. And all the required manifests (serve build and deploy) configuration were located in the manifests/ directory. This will be get used by the Github action workflow to deploy into the KubeRay cluster.

## Manifest files

The manifest files used to deploy the serve app can be found in artifacts on the Github action workflow, This will got essentially used to deploy the asset files.
