package com.example.oz.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

import com.example.oz.config.filter.JWTAuthenticationFilter;

import lombok.RequiredArgsConstructor;


@Configuration //설정 클래스 인식시키기
@EnableWebSecurity //스프링 시큐리티 설정 활성화. 웹 보안관련 설정 기본값 자동적용
@RequiredArgsConstructor
public class SecurityConfig {
	
	private final AuthenticationConfiguration authConfig;
	@Bean
	public PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}
	@Bean
	public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception{
		http.csrf(csrf->csrf.disable());
		http.cors(cors->cors.disable());
		http.authorizeHttpRequests(security->{
			security.requestMatchers("/member/**").authenticated()
			.requestMatchers("/manager/**").hasAnyRole("manager","admin")
			.requestMatchers("/admin/**").hasRole("admin")
			.anyRequest().permitAll();
		});
		http.formLogin(frmLogin->frmLogin.disable());
		http.sessionManagement(ssmg->ssmg.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
		http.addFilter(new JWTAuthenticationFilter(authConfig.getAuthenticationManager()));
		return http.build();
	}
}
