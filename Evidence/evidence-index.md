# Assignment 2 Evidence Index

**Student Name:** Manan Shori  
**Roll Number:** 2025TM93143  
**GitHub Repository:** [https://github.com/mananshori98/aceest-devops](https://github.com/mananshori98/aceest-devops)  
**Docker Hub Repository:** [https://hub.docker.com/r/mananshori98/aceest-fitness-devops](https://hub.docker.com/r/mananshori98/aceest-fitness-devops)  

| No. | Evidence Item | Purpose & Description |
|---|---|---|
| 01 | 01_Git_Baseline_Branch_and_Tests.png | Assignment 1 baseline branch & tag (`assignment-1-final`), backup branch, Assignment 2 feature branch (`feature/assignment-2-cicd`), 19 passing baseline tests on the tag, and clean Git state. Reproduce with `01_baseline_evidence.ps1`. |
| 02 | 02_Local_Pytest_20_Passed_and_Coverage_part_A.png, 02_Local_Pytest_20_Passed_and_Coverage_part_B.png | Python syntax validation (`py_compile`), 20 passing Pytest tests, 91% coverage of `app.py` (part A), and the list of files changed since the Assignment 1 baseline (part B). Reproduce with `02_local_validation_evidence.ps1`. |
| 03 | 03_GitHub_Actions_Success.png | GitHub Actions workflow execution history demonstrating green build status. |
| 04 | 04_GitHub_Actions_Test_and_Build_Success.png | Detailed step logs for syntax validation, Pytest execution, and Docker build/in-container test. |
| 05 | 05_Pull_Request_All_Checks_Passed.png | GitHub Pull Request with automated CI status checks passing without merge conflicts. |
| 06 | 06_Pull_Request_Merged.png | Pull Request merged into `main` branch. |
| 07 | 07_Final_Configuration_PR_Merged.png | Final configuration, documentation, and release tag `assignment-2-v2.0.0` merged. |
| 08 | 08_Docker_Image_Tests_and_Application.png | Local Docker container run, health probes (`/health`, `/ready`), version endpoint (`/version`), and running container. |
| 09 | 09_Docker_Hub_Published_Tags.png | Public Docker Hub repository displaying published tags: `v1.0.0`, `v2.0.0`, and `latest`. |
| 10 | 10_Jenkins_Pipeline_Finished_SUCCESS.png | Jenkins Declarative Pipeline run completed successfully across all stages (`SUCCESS`). |
| 11 | 11_SonarQube_Quality_Gate_Passed.png | SonarQube dashboard showing Quality Gate **PASSED** (0 bugs, 0 vulnerabilities, >80% coverage). |
| 12 | 12_Kubernetes_Base_Deployment_and_Endpoint.png | Kubernetes namespace, pods, service, and live endpoint verification (`base.yaml`). |
| 13A | 13A_Rolling_Update_Passed.png | Kubernetes rolling update triggered with zero downtime and verified rollout status. |
| 13B | 13B_Rollback_Passed.png | Rollback command (`kubectl rollout undo`) executed with immediate restoration of healthy state. |
| 14 | 14_Blue_Green_Traffic_Switch_Passed.png | Blue (`v1.0.0`) and Green (`v2.0.0`) deployment with service selector cutover. |
| 15 | 15_Canary_Deployment_Passed.png | Canary release traffic distribution (75% stable / 25% canary) returning valid responses. |
| 16 | 16_Shadow_Deployment_Validation_Passed.png | Asynchronous traffic mirroring to shadow backend verified via pod access logs. |
| 17 | 17_AB_Testing_Deployment_Passed.png | Header-based routing (`X-ACEEST-Version: B`) directing requests between Version A and Version B. |
| 18 | 18_Jenkins_Poll_SCM_Configured.png | Jenkins Poll SCM configuration screen with cron schedule `H/5 * * * *`. |
