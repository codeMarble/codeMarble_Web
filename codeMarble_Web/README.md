### 문제등록시 주의사항 
```
<problem name>.zip
	L <problem name>.pdf
	L <problem name>.json
```

#### `1. <problem name>.zip`
  problem name.zip파일에는 문제 설명이 나와있는 problem name.pdf, 게임 규칙이 나와있는 problem name.json이 포함되어야 한다.
  .zip, .pdf, .json의 파일이름은 동일해야 한다.

#### `2. <problem name>.pdf`
  It contains problem's descriptions. Problem's few input/output cases can be attached. This will show up on problem page, unless you don't contain this file.

#### `3. <problem name>_SOLUTION | <problem name>_CHECKER`
  It contains its standard file for judging. It can be Solution or Checker up to the meta data in <problem name>.txt file.<br>
  If it is Solution, it will contain
 ```
  -- for each case
  <problem name>_case1_input.txt, 
  <problem name>_case2_input.txt,
  ....
  <problem name>_case1_output.txt,
  <problem name>_case2_output.txt,
  ...
  -- for all cases
  <problme name>_cases_total_inputs.txt
  <problem name>_cases_total_outputs.txt
 ```
  The number of each input case is up to administrator.
  All cases file contains all each case file. 
