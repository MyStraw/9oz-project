package com.example.oz.controller;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.FileCopyUtils;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import com.example.oz.domain.Image;
import com.example.oz.repository.ImageRepository;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class ImageController {
	
	//생성자 주입법 Autowired필드에 쓰지않기
	private final ImageRepository imageRepo;
	
	//전체검색
	@GetMapping("/list")
	public Iterable<Image> getImages(){
		return imageRepo.findAll();
	}
	
	//mainclass로 검색
	@GetMapping("/list/{mainclass}")
    public Iterable<Image> getImagesByMainclass(@PathVariable String mainclass) {
        return imageRepo.findByMainclass(mainclass);
    }

    // semiclass로 검색
    @GetMapping("/list/{mainclass}/{semiclass}")
    public Iterable<Image> getImagesBySemiclass(@PathVariable String mainclass, @PathVariable String semiclass) {
        return imageRepo.findByMainclassAndSemiclass(mainclass, semiclass);
    }
    
    @CrossOrigin(origins = "*")
    @GetMapping("/display") //내 로컬의 이미지를 표시하기
	public ResponseEntity<byte[]> getImage(String fileName){		
		File file = new File("C:/9ozproject/9OZ_SALES/A17/" + fileName);
		
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
	
}
