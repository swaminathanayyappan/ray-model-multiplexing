import yaml
import argparse


def prepare_deployment_config(
        deploy_config_path: str,
        build_config_path: str,
        working_dir: str,
        output_path: str) -> str:
    """
    Function to prepare deployment config file based on build config file

    Parameters
    ----------
        deploy_config_path : str
            Path for serve deploy config file
        build_config_path : str
            Path for serve build config file
        output_path : str
            Path used to store formatted deploy config file
    Returns
    -------
        str
            Path used to store formatted deploy config file
    """

    # Load build config
    with open(build_config_path, "r") as build_config_file:
        build_config = yaml.safe_load(build_config_file)

    # Reading the deployment config
    with open(deploy_config_path, "r") as deploy_config_file:
        deploy_config = yaml.safe_load(deploy_config_file)

    build_spec = build_config.get("applications", None)

    if build_spec:
        for app in build_spec:
            # Setting working_dir for the whole app
            app_runtime_env = app.get("runtime_env", {})
            app_runtime_env["working_dir"] = f'"{working_dir}"'
            # Get the existing dependencies of a application
            app_dependencies = app_runtime_env.get("pip", [])
            for deployment in app.get("deployments"):
                deployment_runtime_env = deployment.get("ray_actor_options")
                deployment_dependencies = deployment_runtime_env.get(
                    "runtime_env").get("pip", [])
                deployment_runtime_env.pop("runtime_env")
                # combine app and deployment dependencies
                combined_dependencies = list(
                    set(app_dependencies + deployment_dependencies)
                    )
                app_runtime_env["pip"] = combined_dependencies

    # print(build_spec)  # List
    build_spec: dict = {"applications": build_spec}

    build_spec_yaml: str = yaml.dump(
        data=build_spec,
        sort_keys=False
    )

    deploy_config["spec"]["serveConfigV2"] = yaml.safe_load(build_spec_yaml)

    multi_lined = yaml.dump(
        deploy_config, sort_keys=False).replace(
        "serveConfigV2:", "serveConfigV2: |").replace("'", "")

    with open(output_path, "w") as file:
        file.write(multi_lined)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "-b",
        "--build-config",
        help="Path for serve build config file",
        type=str,
        required=True
    )
    argparser.add_argument(
        "-d",
        "--deploy-config",
        help="Path for serve deploy config file",
        type=str,
        required=True
    )
    argparser.add_argument(
        "-w",
        "--working-dir",
        help="The asset URL of the github release",
        type=str,
        required=True
    )
    argparser.add_argument(
        "-o",
        "--output-path",
        help="Path used to store formatted deploy config file",
        type=str,
        required=True
    )

    args = argparser.parse_args()
    output_path = prepare_deployment_config(
        args.deploy_config,
        args.build_config,
        args.working_dir,
        args.output_path)
