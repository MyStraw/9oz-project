package com.example.oz;

import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import com.example.oz.domain.Member;
import com.example.oz.repository.MemberRepository;

import jakarta.transaction.Transactional;

@SpringBootTest
public class MemberInitialize {

	@Autowired
	MemberRepository memberRepo;
	
	PasswordEncoder encoder = new BCryptPasswordEncoder();
	
	@Test
	public void doWork() {
		memberRepo.save(Member.builder()
				.username("member")
				.enabled(true)
				.password(encoder.encode("abcd"))
				.role("ROLE_MEMBER")
				.build());
		memberRepo.save(Member.builder()
				.username("manager")
				.enabled(true)
				.password(encoder.encode("abcd"))
				.role("ROLE_MANAGER")
				.build());
		memberRepo.save(Member.builder()
				.username("admin")
				.enabled(true)
				.password(encoder.encode("abcd"))
				.role("ROLE_ADMIN")
				.build());

	}
	
	
}
