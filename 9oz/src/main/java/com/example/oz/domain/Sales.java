package com.example.oz.domain;

import java.util.Date;


import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Data
@Table(name="9oz_sale_data")
public class Sales {
	@Id
	private Long id;
	private Date saledate;
	private Long receipt;
	private String shop_code;
	private String product_code;
	private String product_name;
	private String color_code;
	private String color_name;
	private String size;
	private Long customer_num;
	private Long price;
	private Long quantity;
	
	
}
