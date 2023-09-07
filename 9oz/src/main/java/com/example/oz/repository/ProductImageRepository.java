package com.example.oz.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.querydsl.QuerydslPredicateExecutor;

import com.example.oz.domain.ProductImage;

public interface ProductImageRepository extends JpaRepository<ProductImage, Long>, QuerydslPredicateExecutor<ProductImage> {
	List<ProductImage> findByProductCode(String product_code);
	List<ProductImage> findByProductName(String product_name);
	List<ProductImage> findByProductCodeOrProductName(String product_code, String product_name);
	List<ProductImage> findByImagePath(String imagePath);
}
