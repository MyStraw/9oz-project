package com.example.oz;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import com.example.oz.domain.Member;
import com.example.oz.repository.MemberRepository;

import jakarta.annotation.PostConstruct;

@SpringBootApplication
public class Application {

	@Autowired
	MemberRepository memberRepo;

	PasswordEncoder encoder = new BCryptPasswordEncoder();

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}

//	@PostConstruct
//	public void init() {
//		memberRepo.save(Member.builder().username("member").enabled(true).password(encoder.encode("abcd"))
//				.role("ROLE_MEMBER").build());
//		memberRepo.save(Member.builder().username("manager").enabled(true).password(encoder.encode("abcd"))
//				.role("ROLE_MANAGER").build());
//		memberRepo.save(Member.builder().username("admin").enabled(true).password(encoder.encode("abcd"))
//				.role("ROLE_ADMIN").build());
//	
//	}

}
