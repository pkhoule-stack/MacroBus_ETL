package sn.khoula.macrobus.scheduler;

import org.springframework.batch.core.job.Job;
import org.springframework.batch.core.job.parameters.JobParameters;
import org.springframework.batch.core.job.parameters.JobParametersBuilder;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class EtlScheduler {

    private final JobLauncher jobLauncher;
    private final Job etlJob;

    public EtlScheduler(JobLauncher jobLauncher, Job etlJob) {
        this.jobLauncher = jobLauncher;
        this.etlJob = etlJob;
    }

    @Scheduled(cron = "0 0 2 * * ?")
    public void runEtl() {
        try {
            JobParameters params = new JobParametersBuilder()
                    .addLong("timestamp", System.currentTimeMillis())
                    .toJobParameters();
            jobLauncher.run(etlJob, params);
        } catch (Exception e) {
            throw new RuntimeException("ETL job failed", e);
        }
    }
}
