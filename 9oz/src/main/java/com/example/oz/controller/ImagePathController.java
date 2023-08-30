package com.example.oz.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.oz.domain.ImagePath;
import com.example.oz.repository.ImagePathRepository;

@RestController
public class ImagePathController {

	@Autowired
	private ImagePathRepository imagePathRepo;
	
	@RequestMapping("/imagepath")
	public Iterable<ImagePath> getImagePath(){
		return imagePathRepo.findAll();
	}
}
