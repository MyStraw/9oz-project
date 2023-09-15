package com.example.oz.service;

import java.util.Collections;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.example.oz.domain.Member;
import com.example.oz.repository.MemberRepository;

@Service
public class MemberServiceImpl implements MemberService {

    @Autowired
    private MemberRepository memberRepo;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Member member = memberRepo.findByUsername(username);
        if (member == null) {
            throw new UsernameNotFoundException("User not found");
        }
        return new org.springframework.security.core.userdetails.User(
            member.getUsername(),
            member.getPassword(),
            Collections.singletonList(new SimpleGrantedAuthority("USER"))
        );
    }

    public Member register(Member member) {
        member.setPassword(passwordEncoder.encode(member.getPassword()));
        return memberRepo.save(member);
    }

    @Override
    public Member getMember(String username) {
        return memberRepo.findByUsername(username);
    }
}

