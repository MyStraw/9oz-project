package com.example.oz.controller;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

import org.springframework.data.domain.Sort;
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
import com.example.oz.domain.QProductImage;
import com.example.oz.repository.ProductImageRepository;
import com.querydsl.core.BooleanBuilder;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import reactor.core.publisher.Mono;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
class ProductSearchOption {

	private String sort; //asc , desc , none
	private String sortcolumn; // salePrice, ProductName, totalsale 프론트에서 send할떄 필드이름으로 넘겨주면됨
	private String mainclass; // top(상의),bottom(하의) table codeclass에 필드 mainclass
	private String semiclass; //tshirt... table codeclass에 필드 semiclass
}
@RequiredArgsConstructor
@RestController
public class ProductImageController {
	
	private final ProductImageRepository productImageRepo;
	
	
	@GetMapping("/product/list")
	public List<ProductImage> getProductImages(ProductSearchOption pso){
		System.out.println("getProductImages "+ pso);
		
		BooleanBuilder builder = new BooleanBuilder();
		QProductImage qpi = QProductImage.productImage;
		
		//검색아이템
		if(pso.getMainclass() != null) {
			builder.and(qpi.mainclass.like("%"+pso.getMainclass()+"%"));			
			if(pso.getSemiclass() != null) {
				builder.and(qpi.semiclass.like("%"+pso.getSemiclass()+"%"));	
			}
		}
		//Iterable<ProductImage> iter =  productImageRepo.findAll(builder,Sort.by("salePrice").ascending());
		Sort sort = null;
	    if(pso.getSort() != null && pso.getSortcolumn() != null) {
	        sort = pso.getSort().equalsIgnoreCase("asc") ? Sort.by(pso.getSortcolumn()).ascending() : Sort.by(pso.getSortcolumn()).descending();
	    }

	    Iterable<ProductImage> iter;
	    if(builder.getValue() == null) {
	        iter = sort != null ? productImageRepo.findAll(sort) : productImageRepo.findAll();
	    } else {
	        iter = productImageRepo.findAll(builder, sort != null ? sort : Sort.unsorted());
	    }

	    List<ProductImage> list = StreamSupport.stream(iter.spliterator(), false)
	                                           .collect(Collectors.toList());
	    return list;
	}
	
	//클릭했을때 상세페이지
	@GetMapping("product/list/{product_code}")
	public Iterable<ProductImage> getProductImagesByProductCode(@PathVariable String product_code) {
        return productImageRepo.findByProductCode(product_code);
    }
	
//    @GetMapping("/display") //내 로컬의 이미지를 표시하기
//	public ResponseEntity<byte[]> getImage(String imagePath ){
//		System.out.println("getImage "+ imagePath);
//		
//		File file = new File(imagePath);
//		
//		ResponseEntity<byte[]> result = null;
//		
//		try {
//			HttpHeaders header = new HttpHeaders();
//			
//			header.add("Content-type",Files.probeContentType(file.toPath()));
//			result = new ResponseEntity<>(FileCopyUtils.copyToByteArray(file), header, HttpStatus.OK);			
//			
//		}catch(IOException e) {
//			e.printStackTrace();
//		}
//		return result;		
//	}
	
	// product_code 또는 product_name으로 검색
    @GetMapping("/search")
    public Iterable<ProductImage> getImagesByQuery(@RequestParam String query) {
    	System.out.println("getImagesByQuery "+ query);
        Iterable<ProductImage> results;

        // 먼저 product_code로 검색
        results = productImageRepo.findByProductCode(query);
        
        if (!results.iterator().hasNext()) {  // 결과가 비어있는지 확인
            // product_name으로 검색
            results = productImageRepo.findByProductName(query);
        }
        
        if (!results.iterator().hasNext()) {  // 결과가 비어있는지 확인
            throw new ResponseStatusException(
                  HttpStatus.NOT_FOUND, "No matching product_code or product_name found");
        }
        
        return results;
    }
    
    @PostMapping("/predict")
    public ResponseEntity<String> predictImage(@RequestBody Map<String, String> payload) throws IOException {
    	String imageName = payload.get("image_path");
    	String mainclass = payload.get("mainclass");
    	System.out.println("predictImage " + payload);
    	
        // 이미지 파일을 읽는 코드는 여기에 위치해야 합니다. (예: byte[] imageData = ...)
        byte[] imageData = null; 
        try {
            imageData = Files.readAllBytes(Paths.get(imageName)); // 이미지 파일을 읽는다.
            System.out.println("predictImage " + payload);
        } catch (IOException e) {
            e.printStackTrace();
            return new ResponseEntity<>("Image loading error", HttpStatus.INTERNAL_SERVER_ERROR);
        }
        String base64Encoded = Base64.getEncoder().encodeToString(imageData); // Base64로 인코딩한다.
        
        //WebClient webClient = WebClient.create("http://localhost:5000");
        WebClient webClient = WebClient.create("http://10.125.121.185:5000");
        
        Map<String, String> dataMap = new HashMap<>();
        dataMap.put("image_data", base64Encoded);
        dataMap.put("mainclass", mainclass);
        
        Mono<String> responseMono = webClient.post()
            .uri("/predict")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(dataMap)
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
