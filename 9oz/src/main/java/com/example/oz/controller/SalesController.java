package com.example.oz.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.oz.domain.Sales;
import com.example.oz.repository.SalesRepository;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class SalesController {
	
	
	private final SalesRepository salesRepo;
	
	@RequestMapping("/sales")
	public Iterable<Sales> getSales(){
		return salesRepo.findAll();
	}
}
