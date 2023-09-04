package com.example.oz.repository;

import com.querydsl.core.types.Predicate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.querydsl.QuerydslPredicateExecutor;

import com.example.oz.domain.ProductImage;

public interface DynamicSortRepository extends JpaRepository<ProductImage, Long>, QuerydslPredicateExecutor<ProductImage> {

}
