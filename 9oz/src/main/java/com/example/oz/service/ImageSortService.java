package com.example.oz.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.oz.domain.ProductImage;
import com.example.oz.repository.DynamicSortRepository;
import com.querydsl.core.BooleanBuilder;
import com.querydsl.core.types.Predicate;

@Service
public class ImageSortService {

    @Autowired
    private DynamicSortRepository imageSortRepo;

    public List<ProductImage> findImages(String mainClass, String subClass, String sort) {
        QProductImage qProductImage = QProductImage.productImage;
        BooleanBuilder builder = new BooleanBuilder();

        if (mainClass != null) {
            builder.and(qProductImage.mainClass.eq(mainClass));
        }
        
        if (subClass != null) {
            builder.and(qProductImage.subClass.eq(subClass));
        }

        Predicate predicate = builder.getValue();
        Iterable<ProductImage> images;

        if (sort != null) {
            // sort logic here
        }

        images = imageSortRepo.findAll(predicate);
        
        return Lists.newArrayList(images);
    }
}
