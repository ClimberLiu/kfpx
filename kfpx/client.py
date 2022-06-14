def apply_recurring_run(
    kfp_client,
    experiment_name,
    cron_expression,
    pipeline_package_path,
    job_name,
    enable_caching,
    description,
    params,
) -> any:
    experiment_id = kfp_client.get_experiment(experiment_name=experiment_name).id
    # Delete exists jobs with the same name
    # https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.client.html#kfp.Client.list_recurring_runs
    jobs = kfp_client.list_recurring_runs(
        experiment_id=experiment_id, page_size=10_000
    ).jobs

    if jobs != None:
        matched_jobs = list(filter(lambda j: j.name == job_name, jobs))
        if len(matched_jobs) != 0:
            for j in matched_jobs:
                print(f"Warning: delete exists job: {j.name}")
                kfp_client.delete_job(j.id)

    # https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.client.html#kfp.Client.create_recurring_run
    return kfp_client.create_recurring_run(
        experiment_id=experiment_id,
        job_name=job_name,
        description=description,
        # https://pkg.go.dev/github.com/robfig/cron#hdr-CRON_Expression_Format
        cron_expression=cron_expression,
        max_concurrency=1,
        pipeline_package_path=pipeline_package_path,
        enabled=True,
        enable_caching=enable_caching,
        params=params,
    )
