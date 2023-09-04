package com.example.oz;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import com.example.oz.repository.DynamicSortRepository;

@RunWith(SpringRunner.class)
@SpringBootTest
public class DynamicQueryTest {
	
	private final DynamicSortRepository dynamicSortRepo;
	
	@Test
	public void testDynamicQuery() {
		String mainclass;
		String semiclass;
		String sort;
		String sitem;
		String cond1;
		String cond2;
		String cond3;
		String cond4;
	}
}
