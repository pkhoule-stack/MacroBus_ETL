package sn.khoula.macrobus;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class MacrobusApplication {

    public static void main(String[] args) {
        SpringApplication.run(MacrobusApplication.class, args);
    }

}
