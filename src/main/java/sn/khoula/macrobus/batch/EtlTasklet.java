package sn.khoula.macrobus.batch;

import org.springframework.batch.core.step.StepContribution;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.infrastructure.repeat.RepeatStatus;
import org.springframework.jdbc.core.JdbcTemplate;

import java.util.List;

public class EtlTasklet implements Tasklet {

    private final JdbcTemplate jdbcTemplate;
    private final List<String> sqlStatements;

    public EtlTasklet(JdbcTemplate jdbcTemplate, String sql) {
        this.jdbcTemplate = jdbcTemplate;
        this.sqlStatements = List.of(sql);
    }

    public EtlTasklet(JdbcTemplate jdbcTemplate, List<String> sqlStatements) {
        this.jdbcTemplate = jdbcTemplate;
        this.sqlStatements = sqlStatements;
    }

    @Override
    public RepeatStatus execute(StepContribution contribution, ChunkContext chunkContext) {
        for (String sql : sqlStatements) {
            jdbcTemplate.execute(sql);
        }
        return RepeatStatus.FINISHED;
    }
}
