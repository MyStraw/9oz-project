package com.example.oz.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.oz.domain.Image;

@Repository
public interface ImageRepository extends JpaRepository<Image, Long> {
	List<Image> findByMainclass(String mainclass);
	List<Image> findByMainclassAndSemiclass(String mainclass, String semiclass);
	
	
	
}
