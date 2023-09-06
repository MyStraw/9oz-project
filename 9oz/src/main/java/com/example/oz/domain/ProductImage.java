package com.example.oz.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Table(name="ozsales")
public class ProductImage {
	
//	@Column(nullable = false)
//	private Integer id;
//
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(nullable = false)
	private Integer id;
	
	@Column(nullable = false)
	private String productCode;

	@Column(nullable = false)
	private String productName;

	@Column(nullable = false)
	private String colorName;

	@Column(nullable = false)
	private String size;

	@Column(nullable = false)
	private Integer salePrice;

	@Column(nullable = false)
	private String mainclass;

	@Column(nullable = false)
	private String semiclass;

	@Column(length=1000, nullable = false)
	private String imagePath;
	
	@Column(nullable = false)
	private Integer totalsale;
	
	
}
