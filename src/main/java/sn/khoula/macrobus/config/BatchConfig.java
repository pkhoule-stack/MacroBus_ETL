package sn.khoula.macrobus.config;

import sn.khoula.macrobus.batch.EtlTasklet;
import org.springframework.batch.core.job.Job;
import org.springframework.batch.core.job.builder.JobBuilder;
import org.springframework.batch.core.repository.JobRepository;
import org.springframework.batch.core.step.Step;
import org.springframework.batch.core.step.builder.StepBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.PlatformTransactionManager;

@Configuration
public class BatchConfig {

    @Bean
    public Job etlJob(JobRepository jobRepository, Step cleanupStep,
                      Step dimTempsStep, Step dimVehiculeStep,
                      Step dimCommercialStep, Step dimCommandeStep,
                      Step factVentesStep) {
        return new JobBuilder("etlJob", jobRepository)
                .start(cleanupStep)
                .next(dimTempsStep)
                .next(dimVehiculeStep)
                .next(dimCommercialStep)
                .next(dimCommandeStep)
                .next(factVentesStep)
                .build();
    }

    @Bean
    public Step cleanupStep(JobRepository jobRepository, PlatformTransactionManager transactionManager, EtlTasklet cleanupTasklet) {
        return new StepBuilder("cleanupStep", jobRepository)
                .tasklet(cleanupTasklet, transactionManager)
                .build();
    }

    @Bean
    public Step dimTempsStep(JobRepository jobRepository, PlatformTransactionManager transactionManager, EtlTasklet dimTempsTasklet) {
        return new StepBuilder("dimTempsStep", jobRepository)
                .tasklet(dimTempsTasklet, transactionManager)
                .build();
    }

    @Bean
    public Step dimVehiculeStep(JobRepository jobRepository, PlatformTransactionManager transactionManager, EtlTasklet dimVehiculeTasklet) {
        return new StepBuilder("dimVehiculeStep", jobRepository)
                .tasklet(dimVehiculeTasklet, transactionManager)
                .build();
    }

    @Bean
    public Step dimCommercialStep(JobRepository jobRepository, PlatformTransactionManager transactionManager, EtlTasklet dimCommercialTasklet) {
        return new StepBuilder("dimCommercialStep", jobRepository)
                .tasklet(dimCommercialTasklet, transactionManager)
                .build();
    }

    @Bean
    public Step dimCommandeStep(JobRepository jobRepository, PlatformTransactionManager transactionManager, EtlTasklet dimCommandeTasklet) {
        return new StepBuilder("dimCommandeStep", jobRepository)
                .tasklet(dimCommandeTasklet, transactionManager)
                .build();
    }

    @Bean
    public Step factVentesStep(JobRepository jobRepository, PlatformTransactionManager transactionManager, EtlTasklet factVentesTasklet) {
        return new StepBuilder("factVentesStep", jobRepository)
                .tasklet(factVentesTasklet, transactionManager)
                .build();
    }
}
