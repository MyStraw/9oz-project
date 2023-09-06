package com.example.oz.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QProductImage is a Querydsl query type for ProductImage
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QProductImage extends EntityPathBase<ProductImage> {

    private static final long serialVersionUID = -289952444L;

    public static final QProductImage productImage = new QProductImage("productImage");

    public final StringPath colorName = createString("colorName");

    public final NumberPath<Integer> id = createNumber("id", Integer.class);

    public final StringPath imagePath = createString("imagePath");

    public final StringPath mainclass = createString("mainclass");

    public final StringPath productCode = createString("productCode");

    public final StringPath productName = createString("productName");

    public final NumberPath<Integer> salePrice = createNumber("salePrice", Integer.class);

    public final StringPath semiclass = createString("semiclass");

    public final StringPath size = createString("size");

    public final NumberPath<Integer> totalsale = createNumber("totalsale", Integer.class);

    public QProductImage(String variable) {
        super(ProductImage.class, forVariable(variable));
    }

    public QProductImage(Path<? extends ProductImage> path) {
        super(path.getType(), path.getMetadata());
    }

    public QProductImage(PathMetadata metadata) {
        super(ProductImage.class, metadata);
    }

}

