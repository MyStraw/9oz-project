package com.example.oz.controller;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.Collections;
import java.util.Map;

import org.apache.tomcat.util.http.fileupload.FileUtils;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.FileCopyUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.server.ResponseStatusException;

import com.example.oz.domain.ProductImage;
import com.example.oz.repository.ImageRepository;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Mono;

@RestController
@RequiredArgsConstructor
public class ImageController {
	
	//생성자 주입법 Autowired필드에 쓰지않기
	private final ImageRepository imageRepo;
	
	//전체검색
	@GetMapping("/list")
	public Iterable<ProductImage> getImages(){
		return imageRepo.findAll();
	}
	
	//mainclass로 검색
	@GetMapping("/list/{mainclass}")
    public Iterable<ProductImage> getImagesByMainclass(@PathVariable String mainclass) {
        return imageRepo.findByMainclass(mainclass);
    }

    // semiclass로 검색
    @GetMapping("/list/{mainclass}/{semiclass}")
    public Iterable<ProductImage> getImagesBySemiclass(@PathVariable String mainclass, @PathVariable String semiclass) {
        return imageRepo.findByMainclassAndSemiclass(mainclass, semiclass);
    }
    
 // product_code 또는 product_name으로 검색
    @GetMapping("/search")
    public Iterable<ProductImage> getImagesByQuery(@RequestParam String query) {
        Iterable<ProductImage> results;

        // 먼저 product_code로 검색
        results = imageRepo.findByProductCode(query);
        
        if (!results.iterator().hasNext()) {  // 결과가 비어있는지 확인
            // product_name으로 검색
            results = imageRepo.findByProductName(query);
        }
        
        if (!results.iterator().hasNext()) {  // 결과가 비어있는지 확인
            throw new ResponseStatusException(
                  HttpStatus.NOT_FOUND, "No matching product_code or product_name found");
        }
        
        return results;
    }



   
    
    @GetMapping("/display") //내 로컬의 이미지를 표시하기
	public ResponseEntity<byte[]> getImage(String imagePath){		
		File file = new File(imagePath);
		
		ResponseEntity<byte[]> result = null;
		
		try {
			HttpHeaders header = new HttpHeaders();
			
			header.add("Content-type",Files.probeContentType(file.toPath()));
			
			result = new ResponseEntity<>(FileCopyUtils.copyToByteArray(file), header, HttpStatus.OK);			
			
		}catch(IOException e) {
			e.printStackTrace();
		}
		return result;		
	}
	
    @PostMapping("/predict")
    public ResponseEntity<String> predictImage(@RequestBody Map<String, String> payload) throws IOException {
        String imageName = payload.get("image_path");
        
        // 이미지 파일을 읽는 코드는 여기에 위치해야 합니다. (예: byte[] imageData = ...)
        byte[] imageData = null; 
        try {
            imageData = Files.readAllBytes(Paths.get(imageName)); // 이미지 파일을 읽는다.
        } catch (IOException e) {
            e.printStackTrace();
            return new ResponseEntity<>("Image loading error", HttpStatus.INTERNAL_SERVER_ERROR);
        }
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
