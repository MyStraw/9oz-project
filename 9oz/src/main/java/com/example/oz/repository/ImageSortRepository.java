package com.example.oz.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;


import com.example.oz.domain.ProductImage;

public interface ImageSortRepository extends JpaRepository<ProductImage, Long> {

	@Query("Select p from ProductImage p order by p.totalsale desc")
	List<ProductImage> findByTotalsale();
}
