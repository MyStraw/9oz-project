# 9oz-project
Backend 개발자로서 9oz-project 일지

+ 0818~0825 프로젝트 시작, 대표님과의 대면회의 및 계획서 작성: 이 과정에서 처음부터 어려움을 당면함. 처음 교수님과 대표님과 생각하던 방향이 달라서 이를 하나로 일치시키기 힘들었고, 이 과정에서 나인온스 이미지 데이터를 K-fashion 모델을 돌려서 라벨링 시키고, 신상마켓 이미지를 크롤링해서 다운받아서 k-fashion 모델을 돌려서 라벨링 시켜 같은 라벨을 가진것을 나인온스 이미지를 선택했을때 신상마켓 아이템을 추천하려는 시스템을 구축하기로함.

+ 0828~0901 파이프라인 구축목표: 프론트 <-> 백 <-> 플라스크서버 연동이 되는것을 목표(구현완료). 그 이후 각종 컨트롤러 만들어서 진행 신상마켓이 크롤링을 막아놓은 문제가 발생 -> 퀸잇 사이트로 변경해서 크롤링하기로 함. 이미지 컨트롤러, 분류 컨트롤러 완성.

+ 0904~0905 검색 컨트롤러 완성, 분류와 정렬에 대한 컨트롤러를 하나로 합침(이 과정에서 동적쿼리를 사용, 이렇게 해야 수 많은 경우의 수에 대비해서 쿼리생성이 가능, 프론트에서 값을 찍을때마다 그 값이 쿼리에 들어가게함, 구현하기가 생각보다 힘들었음. 자바 Sort 함수에서 desc, asc 해주는 기능이 있음, 스프링 버그로서 동적쿼리를 만들면 Q도메인이 자동으로 생성되는데 이때 target 밑에도 똑같은것들이 생기는데 이게 already defined가 뜨면서 동적쿼리가 오류가 계속뜸 -> 타겟폴더를 주기적으로 지워주면서 중복오류를 해결)

+ 0906 이미지 파일이 로컬에 저장되어 있고 경로가지고 주고 받고 하다보니 프론트 페이지 로딩때 이미지 로딩때문에 스프링에 부하가 많이 걸림 -> 속도가 느려짐: 이를 해결하기 위해 이미지 파일을 스프링에 resource/static 에 images 폴더를 만들어 놓고 거기다가 이미지를 다 복사해둠 -> 프론트에서 이미지를 불러올 때 스프링에 요청하는것이 아니라 스태틱에 있는 url을 가져감으로써 톰캣서버 전단에서 처리하게 되고 스프링에 대한 부하가 줄어듬 -> 로딩시간 빨리짐(해결)
또한 DB에 테이블내에 ID컬럼이 있는데 스프링서버를 가동하면 컬럼에 동일한 ID컬럼이 생기고 안에 값은 0으로 저장되어있음 -> id 컬럼이 두개가 생기니 프론트에 중복으로 읽히는 버그 발생 -> 지우고 바꿔보고 해봤으나 계속해서 id컬럼이 바뀐 이름따라 생성됨 -> 테이블을 지우고 스프링으로 테이블을 만듬 -> 그 이후 table data import해서 값을 집어 넣음-> 이렇게 하니 스프링서버를 실행시켜도 컬럼이 복사되지않음

+ 0907 /predict 요청시 Flask 서버로 이미지 + mainclass,semiclass 정보 같이 보내주기 -> 기존코드에서
   
	String mainclass = payload.get("mainclass"); 추가
	String semiclass = payload.get("semiclass");

	Map<String, String> dataMap = new HashMap<>();
	dataMap.put("image_data", base64Encoded);
	dataMap.put("mainclass", mainclass); 해쉬맵으로 만들어서 데이터맵에 넣기
	dataMap.put("semiclass", semiclass);

	.bodyValue(dataMap) 밸류를 데이터맵으로 넣기
  
	이렇게 넣어서 받아옴 -> 처음에 None 값으로 계속 들어오길래 오류인줄 알았는데 프론트에서 값을 잘못보낸거였음(해결)
	또 이미지 클릭했을때 이미지의 상세페이지 정보들 불러오는 컨트롤러 설정(product/list/{product_code}로 받아옴)(이미지 클릭시 상품 코드를 찾아서 그에 맞는 상세정보 불러오기)

+ 0908 ~ 0914 JWT를 이용해서 로그인 구현
  
	1.SecurityConfig, JWTAuthorizationFilter, JWTAuthenticationFilter, Member, MemberRepository, MemberService, MemberServiceImpl, SecurityUserDetailsService 설정
  	2.설정 후 test로 db에 member데이터 넣으려는데 junit이 실행이 안됨(정확히는 실행이 되는데 실행이 된 흔적이 없고, db에 저장이 안됨)
  	3.junit이 계속 안되었기에 이를 우회하기 위해
  
  	@PostConstruct
	public void init() {
		memberRepo.save(Member.builder().username("member").enabled(true).password(encoder.encode("abcd"))
				.role("ROLE_MEMBER").build());
		memberRepo.save(Member.builder().username("manager").enabled(true).password(encoder.encode("abcd"))
				.role("ROLE_MANAGER").build());
		memberRepo.save(Member.builder().username("admin").enabled(true).password(encoder.encode("abcd"))
				.role("ROLE_ADMIN").build());
	
	}

 	이 부분을 Application에 넣어두고 처음 실행될때 동작하도록 설정함
	4. 이렇게 하니 member,manager,admin 데이터가 db에 저장되었고 이후 코드부분 주석처리함
  	5. 이후 들어간 데이터와 권한들을 통해 인가 설정(crawl 버튼 기능때문에 권한별 인가 필요)

+ 0915 crawl버튼 활성화 시키기(crawl 버튼은 admin계정만 실행 가능, 실행 시 flask 서버에서 모델링에 필요한 data를 crawling 하고 modeling까지 하는 기능)
  
	@PostMapping("/crawl")
    public ResponseEntity<String> crawling() {
        try {
            String crawlURL = "http://10.125.121.185:5000/crawl";
            HttpHeaders headers = new HttpHeaders();
            headers.set("Content-Type", "application/json");
            HttpEntity<String> entity = new HttpEntity<>(null, headers);
            ResponseEntity<String> resp = restTemplate.exchange(crawlURL, HttpMethod.POST, entity, String.class);
            return ResponseEntity.ok(resp.getBody());
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body("An error occurred: " + e.getMessage());
        }
    }

  1. 먼저 flask서버와 연결하고 HttpHeaders 객체를 생성 후 헤더와 본문을 설정(이 경우 헤더는 null)
  2. restTemplete를 사용해 flask 서버에 post 요청을 보냄(응답은 resp에 저장)
  3. flask 서버로 부터 받은 응답의 본문을 프론트로 반환

------------------------------------
챗지피티 질문방법(패턴) " "부분을 질문전에 넣기


1.페르소나 패턴: 챗지피티가 생성할 응답의 종류와 집중해야 할 세부사항을 안내함 -> 특정 관점이나 견해를 일관되게 채택하도록 맞춤설정가능
Ex)코드검토, 코드버그잡기 => "여러분은 어떤회사의 선임엔지니어입니다. 보안과 성능에 주의를 기울여 다음 코드를 검토하세요. 선임엔지니어라면 해당코드에 대해 생성할 수 있는 출력을 제공하세요."
			이 문장을 먼저 적고 다음에 질문하기 -> 초첨을 맞추고 주목할 대상이 좋아짐
		=> "책 편집자가 되어 가독성에 중점을 두고 다음 블로그 글을 검토해보세요","마케팅 전문가라 생각하고, 다음 슬로건을 검토하고 다른 인기캠페인에 기반하여 개선사항을 제안하세요"
		=> 정해진 주제에 대해서만 얘기해줌

2. 레시피 패턴: 달성하고 싶은 목표가 있고, 재료는 알고 있으며, 달성하기 위한 단계는 어느정도 알고 있지만, 이를 모두 조합하는데 도움이 필요할때 (특히 프로그래머)
ex)케이크를 만들고 싶은데 밀가루, 물, 설탕이 있는데 이를 섞어야 하는것도 알지만 어떻게, 어떤 순서로, 다음에 무엇을 해야 할지 모를때
"데이터를 암호화 하는 Rust 프로그램을 작성하려고 한다. 사용자 입력을 읽고, 유효성을 검사하고, 암호화하고, 암호화한 데이터를 반환해야 한다는것을 알고있다. 
이를 위해 전체단계 순서를 알려주고, 누락된 단계를 채우고, 불필요한 단계가 있는지 확인해주세요."

3. 리플렉션 패턴(주니어개발자들한테 유용) : 모든 답변에 대한 이유를 설명하도록 요청
"답변을 제공할때는 답변의 근거와 가정을 설명하세요. 선택한 사항을 설명하고 잠재적인 제한사항이나 엣지케이스를 설명하세요."

4. 거부차단기 패턴: 지식제한, 안전등의 이유로 답변거부하는것들 => 질문 재구성
"질문에 답할 수 없을때마다 답할 수 없는 이유를 설명하세요. 답변할 수 있는 질문에 대체표현을 하나이상 제공하세요."

5. 뒤집힌 상호작용 패턴 : 역으로 GPT가 질문하게 하기 => 원하는것을 알고 있지만 그 목표를 달성하기 위한 단계를 모르거나 그 목표를 달성하기 위해 GPT가 어떤 정보를 필요로 하는지 모를때 유용
ex)"AWS에 있는 웹서버에 Rust 바이너리를 배포하기위한 질문을 나에게 하세요. 필요한 정보를 모두 얻으면 배포를 자동화하는 bash 스크립트를 작성하세요"
