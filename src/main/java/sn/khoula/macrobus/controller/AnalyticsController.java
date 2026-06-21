package sn.khoula.macrobus.controller;

import sn.khoula.macrobus.service.AnalyticsService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/analytics")
public class AnalyticsController {

    private final AnalyticsService analyticsService;

    public AnalyticsController(AnalyticsService analyticsService) {
        this.analyticsService = analyticsService;
    }

    @GetMapping("/ca-par-commercial")
    public ResponseEntity<?> caParCommercial() {
        return ResponseEntity.ok(analyticsService.caParCommercial());
    }

    @GetMapping("/ca-par-categorie")
    public ResponseEntity<?> caParCategorie() {
        return ResponseEntity.ok(analyticsService.caParCategorie());
    }

    @GetMapping("/ca-par-territoire")
    public ResponseEntity<?> caParTerritoire() {
        return ResponseEntity.ok(analyticsService.caParTerritoire());
    }

    @GetMapping("/ca-par-periode")
    public ResponseEntity<?> caParPeriode() {
        return ResponseEntity.ok(analyticsService.caParPeriode());
    }

    @GetMapping("/top-vehicules")
    public ResponseEntity<?> topVehicules(@RequestParam(defaultValue = "10") int limit) {
        return ResponseEntity.ok(analyticsService.topVehicules(limit));
    }

    @GetMapping("/top-commerciaux")
    public ResponseEntity<?> topCommerciaux(@RequestParam(defaultValue = "5") int limit) {
        return ResponseEntity.ok(analyticsService.topCommerciaux(limit));
    }

    @GetMapping("/performances-commerciaux")
    public ResponseEntity<?> performancesCommerciaux() {
        return ResponseEntity.ok(analyticsService.performancesCommerciaux());
    }

    @GetMapping("/evolution-mensuelle")
    public ResponseEntity<?> evolutionMensuelle() {
        return ResponseEntity.ok(analyticsService.evolutionMensuelle());
    }

    @GetMapping("/ca-par-filiale")
    public ResponseEntity<?> caParFiliale() {
        return ResponseEntity.ok(analyticsService.caParFiliale());
    }

    @GetMapping("/vue-ensemble")
    public ResponseEntity<?> vueEnsemble() {
        return ResponseEntity.ok(analyticsService.vueEnsemble());
    }
}
