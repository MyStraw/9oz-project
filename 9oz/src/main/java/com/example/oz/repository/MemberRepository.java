package com.example.oz.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.oz.domain.Member;

public interface MemberRepository extends JpaRepository<Member, String> {

}
