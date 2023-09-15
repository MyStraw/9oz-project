package com.example.oz.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.SessionAttributes;

import com.example.oz.domain.Member;
import com.example.oz.service.MemberService;

import lombok.RequiredArgsConstructor;

@SessionAttributes("member")
@Controller
@RequiredArgsConstructor
public class LoginController {

	private final MemberService memberService;


    @GetMapping("/register")
    public String registerForm() {
        return "register";
    }

    @PostMapping("/register")
    public String register(Member member) {
    	memberService.register(member);
        return "redirect:/login";
    }
}
