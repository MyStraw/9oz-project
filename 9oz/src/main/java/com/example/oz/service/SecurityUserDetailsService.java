package com.example.oz.service;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.example.oz.domain.Member;
import com.example.oz.repository.MemberRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class SecurityUserDetailsService implements UserDetailsService {

	private final MemberRepository memberRepo;
	

	@Override
	public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
		Member member = memberRepo.findById(username).orElseThrow(()->
		new UsernameNotFoundException("Not Found!"));
		return new User(member.getUsername(), member.getPassword(), member.getAuthorities());
	}
}
