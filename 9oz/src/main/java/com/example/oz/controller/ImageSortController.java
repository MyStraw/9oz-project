package com.example.oz.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.oz.domain.ProductImage;
import com.example.oz.repository.ImageSortRepository;

@RestController
public class ImageSortController {
	
	private final ImageSortRepository imageSortRepo;
	
	public ImageSortController(ImageSortRepository imageSortRepo) {
	    this.imageSortRepo = imageSortRepo;
	}

	@GetMapping("/sort/totalsale")
	public List<ProductImage> getImagesBySortTotalsale(){
		return imageSortRepo.findByTotalsale();
	}
	
	
}
