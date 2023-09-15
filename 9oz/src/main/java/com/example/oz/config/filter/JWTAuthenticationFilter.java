package com.example.oz.config.filter;

import java.io.IOException;
import java.util.Date;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.example.oz.domain.Member;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RequiredArgsConstructor
public class JWTAuthenticationFilter extends UsernamePasswordAuthenticationFilter {

	private final AuthenticationManager authenticationManager;
	
	
	public Authentication attemptAuthentication(HttpServletRequest req, HttpServletResponse resp) throws AuthenticationException{
		ObjectMapper om = new ObjectMapper();
		try {
			Member member = om.readValue(req.getInputStream(),Member.class);
			Authentication authToken = new UsernamePasswordAuthenticationToken(member.getUsername(), member.getPassword());
			Authentication auth = authenticationManager.authenticate(authToken);
			log.info("Authenticated : [" + member.getUsername() + "]");
			return auth;
		}catch (Exception e) {
			log.info("Not Authenticated : " + e.getMessage());
			e.printStackTrace();
		}
		return null;
	}
	
	@Override
	protected void successfulAuthentication(HttpServletRequest req, HttpServletResponse resp, FilterChain chain, Authentication authResult) throws IOException, ServletException{
		User user = (User)authResult.getPrincipal();
		log.info("successfulAuthentication: " + user.toString());
		
		String jwtToken = JWT.create()
							.withClaim("username", user.getUsername())
							.withExpiresAt(new Date(System.currentTimeMillis()+1000*60*30))
							.sign(Algorithm.HMAC256("com.example.oz"));
		resp.addHeader("Authorization", " Bearer " + jwtToken);
		resp.setContentType("application/json");
		resp.setCharacterEncoding("UTF-8");
		resp.getWriter().write("{\"message\":\"로그인 성공\"}");
		resp.getWriter().flush();
		resp.getWriter().close();
//		chain.doFilter(req,resp);
	}
	
}
