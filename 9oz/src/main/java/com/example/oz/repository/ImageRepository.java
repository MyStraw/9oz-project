package com.example.oz.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.oz.domain.ProductImage;

@Repository
public interface ImageRepository extends JpaRepository<ProductImage, Long> {
	List<ProductImage> findByMainclass(String mainclass);
	List<ProductImage> findByMainclassAndSemiclass(String mainclass, String semiclass);
	List<ProductImage> findByProductCode(String product_code);
	List<ProductImage> findByProductName(String product_name);
	List<ProductImage> findByProductCodeOrProductName(String product_code, String product_name);
	
	
}
