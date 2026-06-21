package sn.khoula.macrobus.controller;

import org.springframework.batch.core.job.Job;
import org.springframework.batch.core.job.parameters.JobParameters;
import org.springframework.batch.core.job.parameters.JobParametersBuilder;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/etl")
public class EtlController {

    private final JobLauncher jobLauncher;
    private final Job etlJob;

    public EtlController(JobLauncher jobLauncher, Job etlJob) {
        this.jobLauncher = jobLauncher;
        this.etlJob = etlJob;
    }

    @PostMapping("/run")
    public String runEtl() {
        try {
            JobParameters params = new JobParametersBuilder()
                    .addLong("timestamp", System.currentTimeMillis())
                    .toJobParameters();
            jobLauncher.run(etlJob, params);
            return "ETL job launched successfully";
        } catch (Exception e) {
            return "ETL job failed: " + e.getMessage();
        }
    }
}
