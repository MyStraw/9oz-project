package com.example.oz.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
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
@Table(name="codeclass")
public class ProductImage {
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
	private String salePrice;

	@Column(nullable = false)
	private String mainclass;

	@Column(nullable = false)
	private String semiclass;

	@Column(length=1000, nullable = false)
	private String imagePath;
}
