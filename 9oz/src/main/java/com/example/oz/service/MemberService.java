package com.example.oz.service;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

import com.example.oz.domain.Member;

public interface MemberService {

	Member register(Member member);
    Member getMember(String username);
	UserDetails loadUserByUsername(String username) throws UsernameNotFoundException;

}