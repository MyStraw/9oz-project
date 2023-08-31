package edu.pnu.controller;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.Collections;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.core.publisher.Mono;

@RestController
public class _9ozController {
    public ResponseEntity<String> predictImage(@RequestBody Map<String, String> payload) throws IOException {
        String imageName = payload.get("image_path");
        
        // 이미지 파일을 읽는 코드는 여기에 위치해야 합니다. (예: byte[] imageData = ...)
        byte[] imageData = Files.readAllBytes(Paths.get(imageName)); // 이미지 파일을 읽는다.
        String base64Encoded = Base64.getEncoder().encodeToString(imageData); // Base64로 인코딩한다.
        
        //WebClient webClient = WebClient.create("http://localhost:5000");
        WebClient webClient = WebClient.create("http://10.125.121.185:5000");
        Mono<String> responseMono = webClient.post()
            .uri("/predict")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(Collections.singletonMap("image_data", base64Encoded))
            .retrieve()
            .bodyToMono(String.class);
        
        String response = responseMono.block(); // 비동기 호출을 동기 방식으로 변경
        
        if (response != null) {
            // 플라스크로부터 받은 결과를 프론트엔드에 반환
            return new ResponseEntity<>(response, HttpStatus.OK);
        } else {
            return new ResponseEntity<>("Error", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}