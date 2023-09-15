package com.example.oz.config;

import java.util.Arrays;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import com.example.oz.config.auth.JWTAuthorizationFilter;
import com.example.oz.config.filter.JWTAuthenticationFilter;
import com.example.oz.repository.MemberRepository;

import lombok.RequiredArgsConstructor;

@Configuration // 설정 클래스 인식시키기
@EnableWebSecurity // 스프링 시큐리티 설정 활성화. 웹 보안관련 설정 기본값 자동적용
@RequiredArgsConstructor
public class SecurityConfig {

	private final AuthenticationConfiguration authConfig;
	private final MemberRepository memberRepo;

	@Bean
	public PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}

	@SuppressWarnings("removal")
	@Bean
	public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
		http.csrf(csrf -> csrf.disable());
//		http.cors(cors->cors.disable());
		http.cors();

		http.authorizeHttpRequests(security -> {
			security.requestMatchers("/crawl/**").hasRole("ADMIN")
			.anyRequest().permitAll();
		});
		http.formLogin(frmLogin -> frmLogin.disable());
		http.sessionManagement(ssmg -> ssmg.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
		http.addFilter(new JWTAuthenticationFilter(authConfig.getAuthenticationManager()));
		http.addFilter(new JWTAuthorizationFilter(authConfig.getAuthenticationManager(), memberRepo));
		return http.build();
	}
}
