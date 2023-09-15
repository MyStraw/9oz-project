package com.example.oz.config.auth;

import java.io.IOException;
import java.util.Optional;

import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.example.oz.domain.Member;
import com.example.oz.repository.MemberRepository;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class JWTAuthorizationFilter extends BasicAuthenticationFilter {
	
	private MemberRepository memberRepo;
	
	public JWTAuthorizationFilter(AuthenticationManager authenticationManager, MemberRepository memberRepo) {
		super(authenticationManager);
		this.memberRepo = memberRepo;
	}
	
	@Override
	protected void doFilterInternal(HttpServletRequest req, HttpServletResponse resp, FilterChain chain) throws IOException, ServletException{
		String srcToken = req.getHeader("Authorization");
		if(srcToken == null || !srcToken.startsWith("Bearer ")) {
			chain.doFilter(req, resp);
			return;
		}
		String jwtToken = srcToken.replace("Bearer ", "");
		String username = JWT.require(Algorithm.HMAC256("com.example.oz")).build().verify(jwtToken).getClaim("username").asString();
		Optional<Member> opt = memberRepo.findById(username);
		if(!opt.isPresent()) {
			chain.doFilter(req, resp);
			return;
		}
		
		Member findmember = opt.get();
		User user = new User(findmember.getUsername(), findmember.getPassword(), findmember.getAuthorities());
		Authentication auth = new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
		SecurityContextHolder.getContext().setAuthentication(auth);
		chain.doFilter(req, resp);
	}
}
