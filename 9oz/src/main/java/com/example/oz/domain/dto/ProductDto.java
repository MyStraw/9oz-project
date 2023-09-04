package com.example.oz.domain.dto;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ProductDto {

	@Id
	@Column(nullable = false)
	private Long id;

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
