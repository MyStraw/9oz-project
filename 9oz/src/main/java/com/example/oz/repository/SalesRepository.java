package com.example.oz.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.oz.domain.Sales;

public interface SalesRepository extends JpaRepository<Sales, Long>{
	

}
