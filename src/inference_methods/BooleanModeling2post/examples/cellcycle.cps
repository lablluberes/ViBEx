<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.6 (Build 32) (http://www.copasi.org) at 2012-07-15 04:53:41 UTC -->
<?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="1" versionMinor="0" versionDevel="32">
  <ListOfFunctions>
    <Function key="Function_351" name="Mass_Action_1" type="UserDefined" reversible="unspecified">
      <Expression>
        k1*S1
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_1239" name="k1" order="0" role="variable"/>
        <ParameterDescription key="FunctionParameter_276" name="S1" order="1" role="variable"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_331" name="GK" type="UserDefined" reversible="unspecified">
      <Expression>
        2*A4*A1/(A2-A1+A3*A2+A4*A1+((A2-A1+A3*A2+A4*A1)^2-4*(A2-A1)*A4*A1)^(1/2))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_1238" name="A1" order="0" role="variable"/>
        <ParameterDescription key="FunctionParameter_277" name="A2" order="1" role="variable"/>
        <ParameterDescription key="FunctionParameter_286" name="A3" order="2" role="variable"/>
        <ParameterDescription key="FunctionParameter_264" name="A4" order="3" role="variable"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_37" name="Michaelis-Menten" type="UserDefined" reversible="unspecified">
      <Expression>
        k1*S1*M1/(J1+S1)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_287" name="M1" order="0" role="variable"/>
        <ParameterDescription key="FunctionParameter_921" name="J1" order="1" role="variable"/>
        <ParameterDescription key="FunctionParameter_262" name="k1" order="2" role="variable"/>
        <ParameterDescription key="FunctionParameter_250" name="S1" order="3" role="variable"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_247" name="Mass_Action_2" type="UserDefined" reversible="unspecified">
      <Expression>
        k1*S1*S2
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_254" name="k1" order="0" role="variable"/>
        <ParameterDescription key="FunctionParameter_258" name="S1" order="1" role="variable"/>
        <ParameterDescription key="FunctionParameter_922" name="S2" order="2" role="variable"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_41" name="function_4_Growth" type="UserDefined" reversible="false">
      <Expression>
        mu*MASS
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_1236" name="MASS" order="0" role="product"/>
        <ParameterDescription key="FunctionParameter_275" name="mu" order="1" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_43" name="function_4_Synthesis of CLN2" type="UserDefined" reversible="false">
      <Expression>
        (ksn2_p+ksn2_p_p*(SBF*cell))*MASS
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_261" name="MASS" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_266" name="SBF" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_917" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_265" name="ksn2_p" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_243" name="ksn2_p_p" order="4" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_44" name="function_4_Degradation of CLN2" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdn2,CLN2*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_278" name="CLN2" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_260" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_291" name="kdn2" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="function_4_Synthesis of CLB2" type="UserDefined" reversible="false">
      <Expression>
        (ksb2_p+ksb2_p_p*(MCM1*cell))*MASS
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_268" name="MASS" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_267" name="MCM1" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_288" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_916" name="ksb2_p" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_1235" name="ksb2_p_p" order="4" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_47" name="function_4_Degradation of CLB2" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb2,CLB2*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_272" name="CLB2" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_269" name="Vdb2" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_271" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_48" name="function_4_Synthesis of CLB5" type="UserDefined" reversible="false">
      <Expression>
        (ksb5_p+ksb5_p_p*(SBF*cell))*MASS
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_281" name="MASS" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_282" name="SBF" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_274" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_285" name="ksb5_p" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_283" name="ksb5_p_p" order="4" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="function_4_Degradation of CLB5" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb5,CLB5*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_273" name="CLB5" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_280" name="Vdb5" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_270" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_50" name="function_4_Synthesis of SIC1" type="UserDefined" reversible="false">
      <Expression>
        (ksc1_p+ksc1_p_p*(SWI5*cell))/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_1237" name="SWI5" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_307" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_323" name="ksc1_p" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_296" name="ksc1_p_p" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_51" name="function_4_Phosphorylation of SIC1" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vkpc1,SIC1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_295" name="SIC1" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_299" name="Vkpc1" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_832" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_52" name="function_4_Dephosphorylation of SIC1" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vppc1,SIC1P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_341" name="SIC1P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_298" name="Vppc1" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_297" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_53" name="function_4_Fast Degradation of SIC1P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd3c1,SIC1P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_347" name="SIC1P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_920" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_349" name="kd3c1" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_54" name="function_4_Assoc. of CLB2 and SIC1" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_2(kasb2,CLB2*cell,SIC1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_263" name="CLB2" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_246" name="SIC1" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_313" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_357" name="kasb2" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_55" name="function_4_Dissoc. of CLB2/SIC1 complex" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdib2,C2*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_279" name="C2" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_301" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_363" name="kdib2" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_56" name="function_4_Assoc. of CLB5 and SIC1" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_2(kasb5,CLB5*cell,SIC1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_337" name="CLB5" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_300" name="SIC1" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_328" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_371" name="kasb5" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_57" name="function_4_Dissoc. of CLB5/SIC1" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdib5,C5*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_353" name="C5" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_312" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_377" name="kdib5" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_58" name="function_4_Phosphorylation of C2" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vkpc1,C2*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_381" name="C2" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_343" name="Vkpc1" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_314" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_59" name="function_4_Dephosphorylation of C2P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vppc1,C2P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_387" name="C2P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_362" name="Vppc1" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_336" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_60" name="function_4_Phosphorylation of C5" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vkpc1,C5*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_393" name="C5" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_331" name="Vkpc1" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_329" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_61" name="function_4_Dephosphorylation of C5P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vppc1,C5P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_399" name="C5P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_356" name="Vppc1" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_342" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_62" name="function_4_Degradation of CLB2 in C2" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb2,C2*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_405" name="C2" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_368" name="Vdb2" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_369" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_63" name="function_4_Degradation of CLB5 in C5" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb5,C5*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_411" name="C5" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_376" name="Vdb5" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_330" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_64" name="function_4_Degradation of SIC1 in C2P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd3c1,C2P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_417" name="C2P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_383" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_419" name="kd3c1" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_65" name="function_4_Degradation of SIC1P in C5P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd3c1,C5P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_423" name="C5P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_389" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_425" name="kd3c1" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_66" name="function_4_Degradation of CLB2 in C2P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb2,C2P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_429" name="C2P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_394" name="Vdb2" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_395" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_67" name="function_4_Degradation of CLB5 in C5P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb5,C5P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_435" name="C5P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_401" name="Vdb5" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_382" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_68" name="function_4_CDC6 synthesis" type="UserDefined" reversible="false">
      <Expression>
        (ksf6_p+ksf6_p_p*(SWI5*cell)+ksf6_p_p_p*(SBF*cell))/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_284" name="SBF" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_445" name="SWI5" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_413" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_418" name="ksf6_p" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_437" name="ksf6_p_p" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_400" name="ksf6_p_p_p" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_69" name="function_4_Phosphorylation of CDC6" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vkpf6,CDC6*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_441" name="CDC6" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_355" name="Vkpf6" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_348" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_70" name="function_4_Dephosphorylation of CDC6" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vppf6,CDC6P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_459" name="CDC6P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_1234" name="Vppf6" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_289" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_71" name="function_4_Degradation of CDC6P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd3f6,CDC6P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_465" name="CDC6P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_388" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_467" name="kd3f6" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_72" name="function_4_CLB2/CDC6 complex formation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_2(kasf2,CLB2*cell,CDC6*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_407" name="CDC6" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_473" name="CLB2" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_915" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_475" name="kasf2" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_73" name="function_4_CLB2/CDC6 dissociation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdif2,F2*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_471" name="F2" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_354" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_481" name="kdif2" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_74" name="function_4_CLB5/CDC6 complex formation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_2(kasf5,CLB5*cell,CDC6*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_370" name="CDC6" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_487" name="CLB5" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_406" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_489" name="kasf5" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_75" name="function_4_CLB5/CDC6 dissociation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdif5,F5*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_485" name="F5" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_315" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_495" name="kdif5" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_76" name="function_4_F2 phosphorylation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vkpf6,F2*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_499" name="F2" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_461" name="Vkpf6" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_888" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_77" name="function_4_F2P dephosphorylation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vppf6,F2P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_505" name="F2P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_311" name="Vppf6" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_443" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_78" name="function_4_F5 phosphorylation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vkpf6,F5*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_511" name="F5" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_316" name="Vkpf6" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_317" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_79" name="function_4_F5P dephosphorylation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vppf6,F5P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_517" name="F5P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_474" name="Vppf6" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_460" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_80" name="function_4_CLB2 degradation in F2" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb2,F2*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_523" name="F2" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_486" name="Vdb2" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_480" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_81" name="function_4_CLB5 degradation in F5" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb5,F5*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_529" name="F5" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_494" name="Vdb5" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_444" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_82" name="function_4_CDC6 degradation in F2P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd3f6,F2P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_535" name="F2P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_501" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_537" name="kd3f6" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_83" name="function_4_CDC6 degradation in F5P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd3f6,F5P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_541" name="F5P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_507" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_543" name="kd3f6" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_84" name="function_4_CLB2 degradation in F2P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb2,F2P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_547" name="F2P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_512" name="Vdb2" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_513" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_85" name="function_4_CLB5 degradation in F5P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdb5,F5P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_553" name="F5P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_519" name="Vdb5" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_500" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_86" name="function_4_Synthesis of SWI5" type="UserDefined" reversible="false">
      <Expression>
        (ksswi_p+ksswi_p_p*(MCM1*cell))/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_531" name="MCM1" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_518" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_555" name="ksswi_p" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_536" name="ksswi_p_p" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_87" name="function_4_Degradation of SWI5" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdswi,SWI5*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_327" name="SWI5" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_506" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_569" name="kdswi" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_88" name="function_4_Degradation of SWI5P" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdswi,SWI5P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_573" name="SWI5P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_424" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_575" name="kdswi" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_89" name="function_4_Activation of SWI5" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kaswi*(CDC14*cell),SWI5P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_472" name="CDC14" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_466" name="SWI5P" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_525" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_583" name="kaswi" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_90" name="function_4_Inactivation of SWI5" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kiswi*(CLB2*cell),SWI5*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_574" name="CLB2" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_488" name="SWI5" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_554" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_591" name="kiswi" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_91" name="function_4_Activation of IEP" type="UserDefined" reversible="false">
      <Expression>
        &quot;Michaelis-Menten&quot;(Vaiep,Jaiep,1,IE*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_524" name="IE" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_597" name="Jaiep" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_580" name="Vaiep" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_581" name="cell" order="3" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_92" name="function_4_Inactivation" type="UserDefined" reversible="false">
      <Expression>
        &quot;Michaelis-Menten&quot;(1,Jiiep,kiiep,IEP*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_561" name="IEP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_605" name="Jiiep" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_542" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_607" name="kiiep" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_93" name="function_4_Synthesis of inactive CDC20" type="UserDefined" reversible="false">
      <Expression>
        (ks20_p+ks20_p_p*(MCM1*cell))/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_589" name="MCM1" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_563" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_590" name="ks20_p" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_562" name="ks20_p_p" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_94" name="function_4_Degradation of inactiveCDC20" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd20,CDC20i*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_559" name="CDC20i" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_530" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_621" name="kd20" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_95" name="function_4_Degradation of active CDC20" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd20,CDC20*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_625" name="CDC20" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_568" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_627" name="kd20" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_96" name="function_4_Activation of CDC20" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(ka20_p+ka20_p_p*(IEP*cell),CDC20i*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_604" name="CDC20i" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_613" name="IEP" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_588" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_598" name="ka20_p" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_599" name="ka20_p_p" order="4" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_97" name="function_4_Inactivation_2" type="UserDefined" reversible="false">
      <Expression>
        k*Mass_Action_1(MAD2*cell,CDC20*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_549" name="CDC20" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_643" name="MAD2" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_412" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_645" name="k" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_98" name="function_4_CDH1 synthesis" type="UserDefined" reversible="false">
      <Expression>
        kscdh/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_615" name="cell" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_579" name="kscdh" order="1" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_99" name="function_4_CDH1 degradation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdcdh,CDH1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_653" name="CDH1" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_614" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_655" name="kdcdh" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_100" name="function_4_CDH1i degradation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdcdh,CDH1i*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_659" name="CDH1i" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_582" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_661" name="kdcdh" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_101" name="function_4_CDH1i activation" type="UserDefined" reversible="false">
      <Expression>
        &quot;Michaelis-Menten&quot;(Vacdh,Jacdh,1,CDH1i*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_633" name="CDH1i" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_667" name="Jacdh" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_606" name="Vacdh" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_596" name="cell" order="3" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_102" name="function_4_Inactivation_3" type="UserDefined" reversible="false">
      <Expression>
        &quot;Michaelis-Menten&quot;(Vicdh,Jicdh,1,CDH1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_431" name="CDH1" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_675" name="Jicdh" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_442" name="Vicdh" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_634" name="cell" order="3" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_103" name="function_4_CDC14 synthesis" type="UserDefined" reversible="false">
      <Expression>
        ks14/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_626" name="cell" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_631" name="ks14" order="1" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_104" name="function_4_CDC14 degradation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd14,CDC14*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_685" name="CDC14" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_660" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_687" name="kd14" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_105" name="function_4_Assoc. with NET1 to form RENT" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_2(kasrent,CDC14*cell,NET1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_668" name="CDC14" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_669" name="NET1" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_430" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_695" name="kasrent" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_106" name="function_4_Dissoc. from RENT" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdirent,RENT*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_684" name="RENT" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_548" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_701" name="kdirent" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_107" name="function_4_Assoc with NET1P to form RENTP" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_2(kasrentp,CDC14*cell,NET1P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_620" name="CDC14" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_560" name="NET1P" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_367" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_709" name="kasrentp" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_108" name="function_4_Dissoc. from RENP" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdirentp,RENTP*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_691" name="RENTP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_654" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_715" name="kdirentp" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_109" name="function_4_Net1 synthesis" type="UserDefined" reversible="false">
      <Expression>
        ksnet/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_632" name="cell" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_719" name="ksnet" order="1" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_110" name="function_4_Net1 degradation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdnet,NET1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_723" name="NET1" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_700" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_725" name="kdnet" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_111" name="function_4_Net1P degradation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdnet,NET1P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_729" name="NET1P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_446" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_731" name="kdnet" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_112" name="function_4_NET1 phosphorylation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vkpnet,NET1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_735" name="NET1" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_677" name="Vkpnet" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_666" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_113" name="function_4_dephosphorylation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vppnet,NET1P*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_741" name="NET1P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_706" name="Vppnet" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_707" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_114" name="function_4_RENT phosphorylation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vkpnet,RENT*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_747" name="RENT" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_674" name="Vkpnet" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_644" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_115" name="function_4_dephosphorylation_2" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vppnet,RENTP*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_753" name="RENTP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_714" name="Vppnet" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_676" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_116" name="function_4_Degradation of NET1 in RENT" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdnet,RENT*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_759" name="RENT" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_665" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_761" name="kdnet" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_117" name="function_4_Degradation of NET1P in RENTP" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdnet,RENTP*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_765" name="RENTP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_694" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_767" name="kdnet" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_118" name="function_4_Degradation of CDC14 in RENT" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd14,RENT*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_771" name="RENT" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_737" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_773" name="kd14" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_119" name="function_4_Degradation of CDC14 in RENTP" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kd14,RENTP*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_777" name="RENTP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_724" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_779" name="kd14" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_120" name="function_4_TEM1 activation" type="UserDefined" reversible="false">
      <Expression>
        &quot;Michaelis-Menten&quot;(LTE1*cell,Jatem,1,TEM1GDP*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_736" name="Jatem" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_785" name="LTE1" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_743" name="TEM1GDP" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_787" name="cell" order="3" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_121" name="function_4_inactivation" type="UserDefined" reversible="false">
      <Expression>
        &quot;Michaelis-Menten&quot;(BUB2*cell,Jitem,1,TEM1GTP*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_692" name="BUB2" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_686" name="Jitem" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_755" name="TEM1GTP" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_693" name="cell" order="3" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_122" name="function_4_CDC15 activation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(ka15_p*(TEM1GDP*cell)+ka15_p_p*(TEM1GTP*cell)+ka15p*(CDC14*cell),CDC15i*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_612" name="CDC14" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_290" name="CDC15i" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_795" name="TEM1GDP" order="2" role="modifier"/>
        <ParameterDescription key="FunctionParameter_742" name="TEM1GTP" order="3" role="modifier"/>
        <ParameterDescription key="FunctionParameter_760" name="cell" order="4" role="volume"/>
        <ParameterDescription key="FunctionParameter_793" name="ka15_p" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_1233" name="ka15_p_p" order="6" role="constant"/>
        <ParameterDescription key="FunctionParameter_708" name="ka15p" order="7" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_123" name="function_4_inactivation_2" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(ki15,CDC15*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_722" name="CDC15" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_436" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_705" name="ki15" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_124" name="function_4_PPX synthesis" type="UserDefined" reversible="false">
      <Expression>
        ksppx/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_754" name="cell" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_821" name="ksppx" order="1" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_125" name="function_4_degradation" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdppx,PPX*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_825" name="PPX" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_784" name="Vdppx" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_772" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_126" name="function_4_PDS1 synthesis" type="UserDefined" reversible="false">
      <Expression>
        (kspds_p+ks1pds_p_p*(SBF*cell)+ks2pds_p_p*(MCM1*cell))/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_635" name="MCM1" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_835" name="SBF" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_449" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_837" name="ks1pds_p_p" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_794" name="ks2pds_p_p" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_839" name="kspds_p" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_127" name="function_4_degradation_2" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdpds,PDS1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_831" name="PDS1" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_749" name="Vdpds" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_730" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_128" name="function_4_Degradation of PDS1 in PE" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(Vdpds,PE*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_849" name="PE" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_811" name="Vdpds" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_792" name="cell" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_129" name="function_4_Assoc. with ESP1 to form PE" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_2(kasesp,PDS1*cell,ESP1*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_809" name="ESP1" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_857" name="PDS1" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_748" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_859" name="kasesp" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_130" name="function_4_Disso. from PE" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdiesp,PE*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_855" name="PE" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_292" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_865" name="kdiesp" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_131" name="function_4_DNA synthesis" type="UserDefined" reversible="false">
      <Expression>
        ksori*(eorib5*(CLB5*cell)+eorib2*(CLB2*cell))/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_447" name="CLB2" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_873" name="CLB5" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_806" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_1232" name="eorib2" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_908" name="eorib5" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_877" name="ksori" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_132" name="function_4_Negative regulation of DNA synthesis" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdori,ORI*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_869" name="ORI" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_766" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_871" name="kdori" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_133" name="function_4_Budding" type="UserDefined" reversible="false">
      <Expression>
        ksbud*(ebudn2*(CLN2*cell)+ebudn3*(CLN3*cell)+ebudb5*(CLB5*cell))/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_778" name="CLB5" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_893" name="CLN2" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_833" name="CLN3" order="2" role="modifier"/>
        <ParameterDescription key="FunctionParameter_895" name="cell" order="3" role="volume"/>
        <ParameterDescription key="FunctionParameter_851" name="ebudb5" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_897" name="ebudn2" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_637" name="ebudn3" order="6" role="constant"/>
        <ParameterDescription key="FunctionParameter_899" name="ksbud" order="7" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_134" name="function_4_Negative regulation of Cell budding" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdbud,BUD*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_890" name="BUD" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_923" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_889" name="kdbud" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_135" name="function_4_Spindle formation" type="UserDefined" reversible="false">
      <Expression>
        ksspn*CLB2/(Jspn+CLB2*cell)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_800" name="CLB2" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_448" name="Jspn" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_864" name="cell" order="2" role="volume"/>
        <ParameterDescription key="FunctionParameter_913" name="ksspn" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_136" name="function_4_Spindle disassembly" type="UserDefined" reversible="false">
      <Expression>
        Mass_Action_1(kdspn,SPN*cell)/cell
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_870" name="SPN" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_914" name="cell" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_919" name="kdspn" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_1" name="Chen2004_CellCycle" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="mol" type="deterministic">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_1">
    <dcterms:bibliographicCitation>
      <rdf:Description>
        <CopasiMT:isDescribedBy>
          <rdf:Bag>
            <rdf:li rdf:resource="urn:miriam:pubmed:15169868"/>
          </rdf:Bag>
        </CopasiMT:isDescribedBy>
      </rdf:Description>
    </dcterms:bibliographicCitation>
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2006-05-08T11:05:34Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <dcterms:creator>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>kchen@vt.edu</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Chen</vCard:Family>
                <vCard:Given>Katherine C</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>Department of Biology, Virginia Polytechnic Institute</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>lukas@ebi.ac.uk</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Endler</vCard:Family>
                <vCard:Given>Lukas</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>EMBL-EBI</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>hdharuri@cds.caltech.edu</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Dharuri</vCard:Family>
                <vCard:Given>Harish</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>California Institute of Technology</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:creator>
    <dcterms:modified>
      <rdf:Description>
        <dcterms:W3CDTF>2012-05-15T21:53:24Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:modified>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:biomodels.db:BIOMD0000000056"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:biomodels.db:MODEL6624073334"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.pathway:sce04111"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isHomologTo>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:reactome:REACT_152"/>
      </rdf:Bag>
    </CopasiMT:isHomologTo>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0000278"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
    <CopasiMT:occursIn>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:taxonomy:4932"/>
      </rdf:Bag>
    </CopasiMT:occursIn>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <Comment>
      <body xmlns="http://www.w3.org/1999/xhtml">
  <h1>
				SBML model of Cell cycle control mechanism
			</h1>
  <p>
				This is a hypothetical model of the cell cycle control mechanism by Chen et al(2004). The model reproduces 
				the time profiles of the different species in Fig 2 of the paper. The figure depicts the cycle of a daughter
				cell. Since,the Mass Doubling Time(MDT) is 90 minutes, time t=90 from the model simulation will correspond to 
				time t=0 in the paper. The model was successfully tested using MathSBML  and SBML odeSolver.
        
    
        
        
        
    
        
        
        <br />
				To create valid SBML a local parameter k = 1 was added in reaction: &quot;Inactivation_274_CDC20&quot;.
			</p>
  <p>This model originates from BioModels Database: A Database of Annotated Published Models. It is copyright (c) 2005-2009 The BioModels Team.
        
        
        
    
        
        
        <br />To the extent possible under law, all copyright and related or neighbouring rights to this encoded model have been dedicated to the public domain worldwide. Please refer to <a href="http://creativecommons.org/publicdomain/zero/1.0/" title="Creative Commons CC0">CC0 Public Domain Dedication</a> for more information.</p>
  <p>In summary, you are entitled to use this encoded model in absolutely any manner you deem suitable, verbatim, or with modification, alone or embedded it in a larger context, redistribute it, commercially or not, in a restricted way or not..
        
        
        
    
        
        
        <br />
  <br />
To cite BioModels Database, please use 
        
        
        
    
        
        
        <a href="http://www.pubmedcentral.nih.gov/articlerender.fcgi?tool=pubmed&amp;pubmedid=16381960" target="_blank"> Le Novère N., Bornstein B., Broicher A., Courtot M., Donizelli M., Dharuri H., Li L., Sauro H., Schilstra M., Shapiro B., Snoep J.L., Hucka M. (2006) BioModels Database: A Free, Centralized Database of Curated, Published, Quantitative Kinetic Models of Biochemical and Cellular Systems Nucleic Acids Res., 34: D689-D691.</a>
</p>
</body>
    </Comment>
    <ListOfCompartments>
      <Compartment key="Compartment_0" name="cell" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_0">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_0" name="BCK2" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_0">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P33306" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[b0],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[MASS],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_1" name="BUB2" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_1">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P26448" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_2" name="BUD" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_2">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:cco:CCO%3AC0000485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_3" name="C2" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_3">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P24868" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P24869" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P38634" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_4" name="C2P" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_4">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P24868" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P24869" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P38634" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_5" name="C5" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_5">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P30283" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P32943" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P38634" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_6" name="C5P" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_6">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P30283" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P32943" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P38634" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_7" name="CDC14" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_7">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:Q00684" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_8" name="CDC14T" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_8">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:Q00684" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC14],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[RENT],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[RENTP],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_9" name="CDC15" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_9">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P27636" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_10" name="CDC15i" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_10">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P27636" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[CDC15T],Reference=Value&gt;-&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC15],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_11" name="CDC20" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_11">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P26309" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_12" name="CDC20i" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_12">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P26309" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_13" name="CDC6" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_13">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P09119" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_14" name="CDC6P" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_14">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P09119" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_15" name="CDC6T" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_15">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P09119" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC6],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC6P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F2P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F5P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_16" name="CDH1" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_16">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P53197" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_17" name="CDH1i" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_17">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P53197" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_18" name="CKIT" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_18">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P09119" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P38634" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[SIC1T],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC6T],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_19" name="CLB2" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_19">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P24868" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P24869" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_20" name="CLB2T" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_20">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P24868" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P24869" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C2P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F2P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_21" name="CLB5" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_21">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P30283" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P32943" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_22" name="CLB5T" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_22">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2012-07-14T23:40:27Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P30283" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P32943" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C5P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F5P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_23" name="CLN2" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_23">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2012-07-14T23:29:59Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P20437" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P20438" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_24" name="CLN3" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_24">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P13365" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[C0],Reference=Value&gt;*&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Dn3],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[MASS],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Jn3],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Dn3],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[MASS],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;))/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_25" name="ESP1" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_25">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:Q03018" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_26" name="F2" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_26">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P09119" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P24868" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P24869" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_27" name="F2P" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_27">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P09119" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P24868" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P24869" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_28" name="F5" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_28">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P09119" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P30283" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P32943" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_29" name="F5P" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_29">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P09119" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P30283" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P32943" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_30" name="IE" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_30">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005680" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[IET],Reference=Value&gt;-&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[IEP],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_31" name="IEP" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_31">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005680" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_32" name="LTE1" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_32">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P07866" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_33" name="MAD2" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_33">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P40958" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_34" name="MASS" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_34">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2012-07-14T23:31:18Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.fma:FMA%3A86557" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_35" name="MCM1" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_35">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P11746" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          GK(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kamcm],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;),&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kimcm],Reference=Value&gt;,&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Jamcm],Reference=Value&gt;,&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Jimcm],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_36" name="NET1" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_36">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P47035" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_37" name="NET1P" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_37">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P47035" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_38" name="NET1T" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_38">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P47035" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[NET1],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[NET1P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[RENT],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[RENTP],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_39" name="ORI" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_39">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2012-07-14T23:41:14Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_40" name="PDS1" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_40">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P40316" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_41" name="PE" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_41">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:Q03018" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ESP1T],Reference=Value&gt;-&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[ESP1],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_42" name="PPX" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_42">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P38698" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_43" name="RENT" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_43">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P06700" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P47035" />
        <rdf:li rdf:resource="urn:miriam:uniprot:Q00684" />
      </rdf:Bag>
    </CopasiMT:hasPart>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030869" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_44" name="RENTP" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_44">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P06700" />
        <rdf:li rdf:resource="urn:miriam:uniprot:P47035" />
        <rdf:li rdf:resource="urn:miriam:uniprot:Q00684" />
      </rdf:Bag>
    </CopasiMT:hasPart>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030869" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_45" name="SBF" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_45">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P11938" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          GK(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Vasbf],Reference=Value&gt;,&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Visbf],Reference=Value&gt;,&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Jasbf],Reference=Value&gt;,&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Jisbf],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_46" name="SIC1" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_46">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P38634" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_47" name="SIC1P" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_47">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P38634" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_48" name="SIC1T" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_48">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2012-07-14T23:37:55Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P38634" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[SIC1],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[SIC1P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C2P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C5P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_49" name="SPN" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_49">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:cco:CCO%3AP0000392" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_50" name="SWI5" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_50">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P08153" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_51" name="SWI5P" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_51">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P08153" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_52" name="TEM1GDP" simulationType="assignment" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_52">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P38987" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[TEM1T],Reference=Value&gt;-&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[TEM1GTP],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_53" name="TEM1GTP" simulationType="reactions" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_53">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:uniprot:P38987" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
    </ListOfMetabolites>
    <ListOfModelValues>
      <ModelValue key="ModelValue_0" name="b0" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_1" name="bub2h" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_2" name="bub2l" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_3" name="C0" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_4" name="CDC15T" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_5" name="Dn3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_6" name="ebudb5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_7" name="ebudn2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_8" name="ebudn3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_9" name="ec1b2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_10" name="ec1b5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_11" name="ec1k2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_12" name="ec1n2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_13" name="ec1n3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_14" name="ef6b2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_15" name="ef6b5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_16" name="ef6k2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_17" name="ef6n2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_18" name="ef6n3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_19" name="eicdhb2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_20" name="eicdhb5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_21" name="eicdhn2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_22" name="eicdhn3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_23" name="eorib2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_24" name="eorib5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_25" name="esbfb5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_26" name="esbfn2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_27" name="esbfn3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_28" name="ESP1T" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_29" name="IET" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_30" name="J20ppx" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_31" name="Jacdh" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_32" name="Jaiep" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_33" name="Jamcm" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_34" name="Jasbf" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_35" name="Jatem" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_36" name="Jd2c1" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_37" name="Jd2f6" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_38" name="Jicdh" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_39" name="Jiiep" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_40" name="Jimcm" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_41" name="Jisbf" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_42" name="Jitem" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_43" name="Jn3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_44" name="Jpds" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_45" name="Jspn" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_46" name="ka15'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_47" name="ka15''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_48" name="ka15p" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_49" name="ka20'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_50" name="ka20''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_51" name="kacdh'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_52" name="kacdh''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_53" name="kaiep" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_54" name="kamcm" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_55" name="kasb2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_56" name="kasb5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_57" name="kasbf" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_58" name="kasesp" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_59" name="kasf2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_60" name="kasf5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_61" name="kasrent" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_62" name="kasrentp" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_63" name="kaswi" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_64" name="kd14" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_65" name="kd1c1" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_66" name="kd1f6" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_67" name="kd1pds'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_68" name="kd20" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_69" name="kd2c1" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_70" name="kd2f6" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_71" name="kd2pds''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_72" name="kd3c1" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_73" name="kd3f6" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_74" name="kd3pds''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_75" name="kdb2'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_76" name="kdb2''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_77" name="kdb2p" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_78" name="kdb5'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_79" name="kdb5''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_80" name="kdbud" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_81" name="kdcdh" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_82" name="kdib2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_83" name="kdib5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_84" name="kdiesp" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_85" name="kdif2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_86" name="kdif5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_87" name="kdirent" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_88" name="kdirentp" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_89" name="kdn2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_90" name="kdnet" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_91" name="kdori" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_92" name="kdppx'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_93" name="kdppx''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_94" name="kdspn" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_95" name="kdswi" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_96" name="KEZ" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_97" name="KEZ2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_98" name="ki15" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_99" name="kicdh'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_100" name="kicdh''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_101" name="kiiep" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_102" name="kimcm" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_103" name="kisbf'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_104" name="kisbf''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_105" name="kiswi" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_106" name="kkpnet'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_107" name="kkpnet''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_108" name="kppc1" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_109" name="kppf6" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_110" name="kppnet'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_111" name="kppnet''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_112" name="ks14" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_113" name="ks1pds''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_114" name="ks20'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_115" name="ks20''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_116" name="ks2pds''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_117" name="ksb2'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_118" name="ksb2''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_119" name="ksb5'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_120" name="ksb5''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_121" name="ksbud" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_122" name="ksc1'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_123" name="ksc1''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_124" name="kscdh" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_125" name="ksf6'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_126" name="ksf6''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_127" name="ksf6'''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_128" name="ksn2'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_129" name="ksn2''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_130" name="ksnet" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_131" name="ksori" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_132" name="kspds'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_133" name="ksppx" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_134" name="ksspn" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_135" name="ksswi'" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_136" name="ksswi''" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_137" name="lte1h" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_138" name="lte1l" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_139" name="mad2h" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_140" name="mad2l" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_141" name="mdt" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_142" name="TEM1T" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_143" name="D" simulationType="assignment">
        <Expression>
          1.026/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[mu],Reference=Value&gt;-32
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_144" name="mu" simulationType="assignment">
        <Expression>
          log(2)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[mdt],Reference=Value&gt;
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_145" name="Vdb5" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kdb5&apos;],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kdb5&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC20],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_146" name="Vdb2" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kdb2&apos;],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kdb2&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDH1],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kdb2p],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC20],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_147" name="Vasbf" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kasbf],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[esbfn2],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLN2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[esbfn3],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLN3],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[BCK2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[esbfb5],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;))
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_148" name="Visbf" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kisbf&apos;],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kisbf&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_149" name="Vkpc1" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kd1c1],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Vd2c1],Reference=Value&gt;/(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Jd2c1],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[SIC1],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[SIC1P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C2P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[C5P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_150" name="Vkpf6" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kd1f6],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Vd2f6],Reference=Value&gt;/(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Jd2f6],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC6],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC6P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F2P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[F5P],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_151" name="Vacdh" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kacdh&apos;],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kacdh&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC14],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_152" name="Vicdh" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kicdh&apos;],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kicdh&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[eicdhn3],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLN3],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[eicdhn2],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLN2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[eicdhb5],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[eicdhb2],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;))
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_153" name="Vppnet" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kppnet&apos;],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kppnet&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[PPX],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_154" name="Vkpnet" simulationType="assignment">
        <Expression>
          (&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kkpnet&apos;],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kkpnet&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC15],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;))*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[MASS],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_155" name="Vdppx" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kdppx&apos;],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kdppx&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[J20ppx],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC20],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)*&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Jpds],Reference=Value&gt;/(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[Jpds],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[PDS1],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_156" name="Vdpds" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kd1pds&apos;],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kd2pds&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC20],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kd3pds&apos;&apos;],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDH1],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_157" name="Vaiep" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kaiep],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_158" name="Vd2c1" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kd2c1],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ec1n3],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLN3],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ec1k2],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[BCK2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ec1n2],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLN2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ec1b5],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ec1b2],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;))
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_159" name="Vd2f6" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kd2f6],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ef6n3],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLN3],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ef6k2],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[BCK2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ef6n2],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLN2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ef6b5],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[ef6b2],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;))
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_160" name="Vppc1" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kppc1],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC14],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_161" name="Vppf6" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[kppf6],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDC14],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_162" name="F" simulationType="assignment">
        <Expression>
          exp(-&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[mu],Reference=Value&gt;*&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[D],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_163" name="amount to particle factor" simulationType="fixed">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_0" name="Growth" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_0">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0016049" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_34" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_520" name="mu" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_41">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_1236">
              <SourceParameter reference="Metabolite_34"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="ModelValue_144"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1" name="Synthesis of CLN2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_1">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.pathway:sce04110" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_23" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_45" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_34" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_521" name="ksn2_p" value="1"/>
          <Constant key="Parameter_522" name="ksn2_p_p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_43">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_261">
              <SourceParameter reference="Metabolite_34"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="Metabolite_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_917">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="ModelValue_128"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_243">
              <SourceParameter reference="ModelValue_129"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_2" name="Degradation of CLN2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_2">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_23" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_523" name="kdn2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_44">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Metabolite_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_260">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_291">
              <SourceParameter reference="ModelValue_89"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_3" name="Synthesis of CLB2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_3">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_19" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_35" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_34" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_524" name="ksb2_p" value="1"/>
          <Constant key="Parameter_525" name="ksb2_p_p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_45">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Metabolite_34"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Metabolite_35"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_916">
              <SourceParameter reference="ModelValue_117"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_1235">
              <SourceParameter reference="ModelValue_118"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_4" name="Degradation of CLB2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_4">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_19" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_526" name="Vdb2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_47">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="Metabolite_19"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="ModelValue_146"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_5" name="Synthesis of CLB5" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_5">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_45" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_34" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_527" name="ksb5_p" value="1"/>
          <Constant key="Parameter_528" name="ksb5_p_p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_48">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Metabolite_34"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="Metabolite_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="ModelValue_119"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="ModelValue_120"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_6" name="Degradation of CLB5" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_6">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_529" name="Vdb5" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_49">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="ModelValue_145"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_7" name="Synthesis of SIC1" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_7">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_46" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_50" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_530" name="ksc1_p" value="1"/>
          <Constant key="Parameter_531" name="ksc1_p_p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_50">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_1237">
              <SourceParameter reference="Metabolite_50"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_307">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_323">
              <SourceParameter reference="ModelValue_122"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_296">
              <SourceParameter reference="ModelValue_123"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_8" name="Phosphorylation of SIC1" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_8">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.22" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004693" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_46" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_532" name="Vkpc1" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_51">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_295">
              <SourceParameter reference="Metabolite_46"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_299">
              <SourceParameter reference="ModelValue_149"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_832">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_9" name="Dephosphorylation of SIC1" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_9">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.1.3.48" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004721" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_46" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_533" name="Vppc1" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_52">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_341">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_298">
              <SourceParameter reference="ModelValue_160"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_297">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_10" name="Fast Degradation of SIC1P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_10">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_534" name="kd3c1" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_53">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_347">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_920">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_349">
              <SourceParameter reference="ModelValue_72"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_11" name="Assoc. of CLB2 and SIC1" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_11">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005515" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_19" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_46" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_537" name="kasb2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_54">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_263">
              <SourceParameter reference="Metabolite_19"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="Metabolite_46"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_313">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_357">
              <SourceParameter reference="ModelValue_55"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_12" name="Dissoc. of CLB2/SIC1 complex" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_12">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043624" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_19" stoichiometry="1"/>
          <Product metabolite="Metabolite_46" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_536" name="kdib2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_55">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_301">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_363">
              <SourceParameter reference="ModelValue_82"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_13" name="Assoc. of CLB5 and SIC1" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_13">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005515" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_46" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_535" name="kasb5" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_56">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_337">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_300">
              <SourceParameter reference="Metabolite_46"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_328">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_371">
              <SourceParameter reference="ModelValue_56"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_14" name="Dissoc. of CLB5/SIC1" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_14">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043624" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
          <Product metabolite="Metabolite_46" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_538" name="kdib5" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_57">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_353">
              <SourceParameter reference="Metabolite_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_312">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_377">
              <SourceParameter reference="ModelValue_83"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_15" name="Phosphorylation of C2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_15">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.22" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004693" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_4" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_539" name="Vkpc1" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_58">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_381">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_343">
              <SourceParameter reference="ModelValue_149"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_314">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_16" name="Dephosphorylation of C2P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_16">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.1.3.48" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004721" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_4" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_541" name="Vppc1" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_59">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_387">
              <SourceParameter reference="Metabolite_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_362">
              <SourceParameter reference="ModelValue_160"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_336">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_17" name="Phosphorylation of C5" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_17">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.22" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004693" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_6" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_540" name="Vkpc1" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_60">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_393">
              <SourceParameter reference="Metabolite_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_331">
              <SourceParameter reference="ModelValue_149"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_329">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_18" name="Dephosphorylation of C5P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_18">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.1.3.48" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004721" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_6" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_542" name="Vppc1" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_61">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_399">
              <SourceParameter reference="Metabolite_6"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_356">
              <SourceParameter reference="ModelValue_160"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_342">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_19" name="Degradation of CLB2 in C2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_19">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_46" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_545" name="Vdb2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_62">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_405">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_368">
              <SourceParameter reference="ModelValue_146"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_369">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_20" name="Degradation of CLB5 in C5" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_20">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_46" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_544" name="Vdb5" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_63">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_411">
              <SourceParameter reference="Metabolite_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_376">
              <SourceParameter reference="ModelValue_145"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_330">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_21" name="Degradation of SIC1 in C2P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_21">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_4" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_19" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_543" name="kd3c1" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_64">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_417">
              <SourceParameter reference="Metabolite_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_383">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_419">
              <SourceParameter reference="ModelValue_72"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_22" name="Degradation of SIC1P in C5P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_22">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_6" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_546" name="kd3c1" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_65">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_423">
              <SourceParameter reference="Metabolite_6"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_389">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_425">
              <SourceParameter reference="ModelValue_72"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_23" name="Degradation of CLB2 in C2P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_23">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_4" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_547" name="Vdb2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_66">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_429">
              <SourceParameter reference="Metabolite_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_394">
              <SourceParameter reference="ModelValue_146"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_395">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_24" name="Degradation of CLB5 in C5P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_24">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_6" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_548" name="Vdb5" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_67">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_435">
              <SourceParameter reference="Metabolite_6"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_401">
              <SourceParameter reference="ModelValue_145"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_382">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_25" name="CDC6 synthesis" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_25">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_50" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_45" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_549" name="ksf6_p" value="1"/>
          <Constant key="Parameter_550" name="ksf6_p_p" value="1"/>
          <Constant key="Parameter_551" name="ksf6_p_p_p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_68">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Metabolite_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_445">
              <SourceParameter reference="Metabolite_50"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_413">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_418">
              <SourceParameter reference="ModelValue_125"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_437">
              <SourceParameter reference="ModelValue_126"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_400">
              <SourceParameter reference="ModelValue_127"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_26" name="Phosphorylation of CDC6" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_26">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.22" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004693" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_14" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_552" name="Vkpf6" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_69">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_441">
              <SourceParameter reference="Metabolite_13"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_355">
              <SourceParameter reference="ModelValue_150"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_348">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_27" name="Dephosphorylation of CDC6" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_27">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.1.3.48" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004721" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_14" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_553" name="Vppf6" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_70">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_459">
              <SourceParameter reference="Metabolite_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_1234">
              <SourceParameter reference="ModelValue_161"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_28" name="Degradation of CDC6P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_28">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_14" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_554" name="kd3f6" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_71">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_465">
              <SourceParameter reference="Metabolite_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_388">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_467">
              <SourceParameter reference="ModelValue_73"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_29" name="CLB2/CDC6 complex formation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_29">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005515" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_19" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_26" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_555" name="kasf2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_72">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_407">
              <SourceParameter reference="Metabolite_13"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_473">
              <SourceParameter reference="Metabolite_19"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_915">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_475">
              <SourceParameter reference="ModelValue_59"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_30" name="CLB2/CDC6 dissociation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_30">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043624" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_26" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_19" stoichiometry="1"/>
          <Product metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_556" name="kdif2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_73">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_471">
              <SourceParameter reference="Metabolite_26"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_354">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_481">
              <SourceParameter reference="ModelValue_85"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_31" name="CLB5/CDC6 complex formation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_31">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005515" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_28" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_557" name="kasf5" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_74">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_370">
              <SourceParameter reference="Metabolite_13"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_487">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_406">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_489">
              <SourceParameter reference="ModelValue_60"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_32" name="CLB5/CDC6 dissociation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_32">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043624" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_28" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
          <Product metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_558" name="kdif5" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_75">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_485">
              <SourceParameter reference="Metabolite_28"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_315">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_495">
              <SourceParameter reference="ModelValue_86"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_33" name="F2 phosphorylation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_33">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.22" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004693" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_26" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_27" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_559" name="Vkpf6" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_76">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_499">
              <SourceParameter reference="Metabolite_26"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_461">
              <SourceParameter reference="ModelValue_150"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_888">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_34" name="F2P dephosphorylation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_34">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.1.3.48" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004721" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_27" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_26" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_560" name="Vppf6" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_77">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_505">
              <SourceParameter reference="Metabolite_27"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_311">
              <SourceParameter reference="ModelValue_161"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_443">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_35" name="F5 phosphorylation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_35">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.22" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004693" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_28" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_29" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_561" name="Vkpf6" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_78">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_511">
              <SourceParameter reference="Metabolite_28"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_316">
              <SourceParameter reference="ModelValue_150"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_317">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_36" name="F5P dephosphorylation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_36">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.1.3.48" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004721" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_29" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_28" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_565" name="Vppf6" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_79">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_517">
              <SourceParameter reference="Metabolite_29"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_474">
              <SourceParameter reference="ModelValue_161"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_460">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_37" name="CLB2 degradation in F2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_37">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_26" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_566" name="Vdb2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_80">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_523">
              <SourceParameter reference="Metabolite_26"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_486">
              <SourceParameter reference="ModelValue_146"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_480">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_38" name="CLB5 degradation in F5" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_38">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_28" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_562" name="Vdb5" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_81">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_529">
              <SourceParameter reference="Metabolite_28"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_494">
              <SourceParameter reference="ModelValue_145"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_444">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_39" name="CDC6 degradation in F2P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_39">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_27" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_19" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_563" name="kd3f6" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_82">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_535">
              <SourceParameter reference="Metabolite_27"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_501">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_537">
              <SourceParameter reference="ModelValue_73"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_40" name="CDC6 degradation in F5P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_40">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_29" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_564" name="kd3f6" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_83">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_541">
              <SourceParameter reference="Metabolite_29"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_507">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_543">
              <SourceParameter reference="ModelValue_73"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_41" name="CLB2 degradation in F2P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_41">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_27" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_14" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_567" name="Vdb2" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_84">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_547">
              <SourceParameter reference="Metabolite_27"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_512">
              <SourceParameter reference="ModelValue_146"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_513">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_42" name="CLB5 degradation in F5P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_42">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008054" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_29" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_14" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_658" name="Vdb5" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_85">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_553">
              <SourceParameter reference="Metabolite_29"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_519">
              <SourceParameter reference="ModelValue_145"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_500">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_43" name="Synthesis of SWI5" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_43">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_50" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_35" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_657" name="ksswi_p" value="1"/>
          <Constant key="Parameter_334" name="ksswi_p_p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_86">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_531">
              <SourceParameter reference="Metabolite_35"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_518">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_555">
              <SourceParameter reference="ModelValue_135"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_536">
              <SourceParameter reference="ModelValue_136"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_44" name="Degradation of SWI5" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_44">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_50" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_335" name="kdswi" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_87">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_327">
              <SourceParameter reference="Metabolite_50"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_506">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_569">
              <SourceParameter reference="ModelValue_95"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_45" name="Degradation of SWI5P" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_45">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_51" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_333" name="kdswi" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_88">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_573">
              <SourceParameter reference="Metabolite_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_424">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_575">
              <SourceParameter reference="ModelValue_95"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_46" name="Activation of SWI5" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_46">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.1.3.48" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004721" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051091" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_51" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_50" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_656" name="kaswi" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_89">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_472">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_466">
              <SourceParameter reference="Metabolite_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_525">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_583">
              <SourceParameter reference="ModelValue_63"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_47" name="Inactivation of SWI5" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_47">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.22" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004693" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043433" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_50" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_51" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_19" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_332" name="kiswi" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_90">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_574">
              <SourceParameter reference="Metabolite_19"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_488">
              <SourceParameter reference="Metabolite_50"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_554">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_591">
              <SourceParameter reference="ModelValue_105"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_48" name="Activation of IEP" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_48">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.22" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004693" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_30" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_31" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_512" name="Jaiep" value="1"/>
          <Constant key="Parameter_511" name="Vaiep" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_91">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_524">
              <SourceParameter reference="Metabolite_30"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_597">
              <SourceParameter reference="ModelValue_32"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_580">
              <SourceParameter reference="ModelValue_157"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_581">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_49" name="Inactivation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_49">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0001100" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_31" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_30" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_568" name="Jiiep" value="1"/>
          <Constant key="Parameter_569" name="kiiep" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_92">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_561">
              <SourceParameter reference="Metabolite_31"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_605">
              <SourceParameter reference="ModelValue_39"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_542">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_607">
              <SourceParameter reference="ModelValue_101"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_50" name="Synthesis of inactive CDC20" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_50">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_12" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_35" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_330" name="ks20_p" value="1"/>
          <Constant key="Parameter_331" name="ks20_p_p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_93">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_589">
              <SourceParameter reference="Metabolite_35"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_563">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_590">
              <SourceParameter reference="ModelValue_114"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_562">
              <SourceParameter reference="ModelValue_115"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_51" name="Degradation of inactiveCDC20" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_51">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_12" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_316" name="kd20" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_94">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_559">
              <SourceParameter reference="Metabolite_12"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_530">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_621">
              <SourceParameter reference="ModelValue_68"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_52" name="Degradation of active CDC20" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_52">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_315" name="kd20" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_95">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_625">
              <SourceParameter reference="Metabolite_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_568">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_627">
              <SourceParameter reference="ModelValue_68"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_53" name="Activation of CDC20" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_53">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0031536" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_12" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_31" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_314" name="ka20_p" value="1"/>
          <Constant key="Parameter_317" name="ka20_p_p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_96">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_604">
              <SourceParameter reference="Metabolite_12"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_613">
              <SourceParameter reference="Metabolite_31"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_588">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_598">
              <SourceParameter reference="ModelValue_49"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_599">
              <SourceParameter reference="ModelValue_50"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_54" name="Inactivation_2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_54">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0001100" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_12" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_33" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_318" name="k" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_97">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_549">
              <SourceParameter reference="Metabolite_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_643">
              <SourceParameter reference="Metabolite_33"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_412">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_645">
              <SourceParameter reference="Parameter_318"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_55" name="CDH1 synthesis" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_55">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_16" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_319" name="kscdh" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_98">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_615">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_579">
              <SourceParameter reference="ModelValue_124"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_56" name="CDH1 degradation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_56">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_16" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_320" name="kdcdh" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_99">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_653">
              <SourceParameter reference="Metabolite_16"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_614">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_655">
              <SourceParameter reference="ModelValue_81"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_57" name="CDH1i degradation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_57">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_321" name="kdcdh" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_100">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_659">
              <SourceParameter reference="Metabolite_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_582">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_661">
              <SourceParameter reference="ModelValue_81"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_58" name="CDH1i activation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_58">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.1.3.48" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004721" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0031536" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_16" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_322" name="Jacdh" value="1"/>
          <Constant key="Parameter_323" name="Vacdh" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_101">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_633">
              <SourceParameter reference="Metabolite_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_667">
              <SourceParameter reference="ModelValue_31"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_606">
              <SourceParameter reference="ModelValue_151"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_596">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_59" name="Inactivation_3" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_59">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.22" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0001100" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004693" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_16" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_324" name="Jicdh" value="1"/>
          <Constant key="Parameter_325" name="Vicdh" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_102">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_431">
              <SourceParameter reference="Metabolite_16"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_675">
              <SourceParameter reference="ModelValue_38"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_442">
              <SourceParameter reference="ModelValue_152"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_634">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_60" name="CDC14 synthesis" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_60">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_326" name="ks14" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_103">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_626">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_631">
              <SourceParameter reference="ModelValue_112"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_61" name="CDC14 degradation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_61">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_327" name="kd14" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_104">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_685">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_660">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_687">
              <SourceParameter reference="ModelValue_64"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_62" name="Assoc. with NET1 to form RENT" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_62">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005515" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030869" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_36" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_43" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_329" name="kasrent" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_105">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_668">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_669">
              <SourceParameter reference="Metabolite_36"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_430">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_695">
              <SourceParameter reference="ModelValue_61"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_63" name="Dissoc. from RENT" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_63">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043624" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_43" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_36" stoichiometry="1"/>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_328" name="kdirent" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_106">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_684">
              <SourceParameter reference="Metabolite_43"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_548">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_701">
              <SourceParameter reference="ModelValue_87"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_64" name="Assoc with NET1P to form RENTP" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_64">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.pathway:ko04111" />
      </rdf:Bag>
    </CopasiMT:hasPart>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005515" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_44" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_510" name="kasrentp" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_107">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_620">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_560">
              <SourceParameter reference="Metabolite_37"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_367">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_709">
              <SourceParameter reference="ModelValue_62"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_65" name="Dissoc. from RENP" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_65">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043624" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_44" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
          <Product metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_509" name="kdirentp" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_108">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_691">
              <SourceParameter reference="Metabolite_44"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_654">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_715">
              <SourceParameter reference="ModelValue_88"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_66" name="Net1 synthesis" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_66">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_36" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_508" name="ksnet" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_109">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_632">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_719">
              <SourceParameter reference="ModelValue_130"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_67" name="Net1 degradation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_67">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_36" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_507" name="kdnet" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_110">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_723">
              <SourceParameter reference="Metabolite_36"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_700">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_725">
              <SourceParameter reference="ModelValue_90"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_68" name="Net1P degradation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_68">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_506" name="kdnet" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_111">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_729">
              <SourceParameter reference="Metabolite_37"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_446">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_731">
              <SourceParameter reference="ModelValue_90"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_69" name="NET1 phosphorylation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_69">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.1" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004672" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0031536" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_36" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_505" name="Vkpnet" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_112">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_735">
              <SourceParameter reference="Metabolite_36"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_677">
              <SourceParameter reference="ModelValue_154"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_666">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_70" name="dephosphorylation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_70">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.6.1.11" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004309" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_36" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_504" name="Vppnet" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_113">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_741">
              <SourceParameter reference="Metabolite_37"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_706">
              <SourceParameter reference="ModelValue_153"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_707">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_71" name="RENT phosphorylation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_71">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.1" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004672" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006468" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0031536" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_43" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_44" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_503" name="Vkpnet" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_114">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_747">
              <SourceParameter reference="Metabolite_43"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_674">
              <SourceParameter reference="ModelValue_154"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_644">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_72" name="dephosphorylation_2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_72">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.6.1.11" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004309" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_44" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_43" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_502" name="Vppnet" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_115">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_753">
              <SourceParameter reference="Metabolite_44"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_714">
              <SourceParameter reference="ModelValue_153"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_676">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_73" name="Degradation of NET1 in RENT" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_73">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_43" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_501" name="kdnet" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_116">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_759">
              <SourceParameter reference="Metabolite_43"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_665">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_761">
              <SourceParameter reference="ModelValue_90"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_74" name="Degradation of NET1P in RENTP" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_74">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_44" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_500" name="kdnet" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_117">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_765">
              <SourceParameter reference="Metabolite_44"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_694">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_767">
              <SourceParameter reference="ModelValue_90"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_75" name="Degradation of CDC14 in RENT" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_75">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_43" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_36" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_499" name="kd14" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_118">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_771">
              <SourceParameter reference="Metabolite_43"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_737">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_773">
              <SourceParameter reference="ModelValue_64"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_76" name="Degradation of CDC14 in RENTP" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_76">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_44" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_498" name="kd14" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_119">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_777">
              <SourceParameter reference="Metabolite_44"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_724">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_779">
              <SourceParameter reference="ModelValue_64"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_77" name="TEM1 activation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_77">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005515" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005525" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0031536" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_52" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_53" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_32" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_497" name="Jatem" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_120">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_736">
              <SourceParameter reference="ModelValue_35"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_785">
              <SourceParameter reference="Metabolite_32"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_743">
              <SourceParameter reference="Metabolite_52"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_787">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_78" name="inactivation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_78">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005096" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005515" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0007094" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_53" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_52" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_496" name="Jitem" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_121">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_692">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_686">
              <SourceParameter reference="ModelValue_42"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_755">
              <SourceParameter reference="Metabolite_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_693">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_79" name="CDC15 activation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_79">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.1" />
        <rdf:li rdf:resource="urn:miriam:ec-code:3.1.3.48" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0004721" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006470" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0031536" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_10" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_52" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_53" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_495" name="ka15_p" value="1"/>
          <Constant key="Parameter_494" name="ka15_p_p" value="1"/>
          <Constant key="Parameter_493" name="ka15p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_122">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_612">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Metabolite_10"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_795">
              <SourceParameter reference="Metabolite_52"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_742">
              <SourceParameter reference="Metabolite_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_760">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_793">
              <SourceParameter reference="ModelValue_46"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_1233">
              <SourceParameter reference="ModelValue_47"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_708">
              <SourceParameter reference="ModelValue_48"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_80" name="inactivation_2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_80">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.11.1" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0001100" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006469" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_10" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_492" name="ki15" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_123">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_722">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_436">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_705">
              <SourceParameter reference="ModelValue_98"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_81" name="PPX synthesis" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_81">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.6.1.11" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_42" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_491" name="ksppx" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_124">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_754">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_821">
              <SourceParameter reference="ModelValue_133"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_82" name="degradation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_82">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_42" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_490" name="Vdppx" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_125">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_825">
              <SourceParameter reference="Metabolite_42"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_784">
              <SourceParameter reference="ModelValue_155"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_772">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_83" name="PDS1 synthesis" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_83">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006412" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_40" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_45" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_35" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_489" name="ks1pds_p_p" value="1"/>
          <Constant key="Parameter_488" name="ks2pds_p_p" value="1"/>
          <Constant key="Parameter_487" name="kspds_p" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_126">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_635">
              <SourceParameter reference="Metabolite_35"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_835">
              <SourceParameter reference="Metabolite_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_449">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_837">
              <SourceParameter reference="ModelValue_113"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_794">
              <SourceParameter reference="ModelValue_116"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_839">
              <SourceParameter reference="ModelValue_132"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_84" name="degradation_2" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_84">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_40" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_486" name="Vdpds" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_127">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_831">
              <SourceParameter reference="Metabolite_40"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_749">
              <SourceParameter reference="ModelValue_156"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_730">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_85" name="Degradation of PDS1 in PE" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_85">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0030163" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051437" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_41" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_25" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_485" name="Vdpds" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_128">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_849">
              <SourceParameter reference="Metabolite_41"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_811">
              <SourceParameter reference="ModelValue_156"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_792">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_86" name="Assoc. with ESP1 to form PE" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_86">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005515" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043027" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_40" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_25" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_41" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_484" name="kasesp" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_129">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_809">
              <SourceParameter reference="Metabolite_25"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_857">
              <SourceParameter reference="Metabolite_40"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_748">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_859">
              <SourceParameter reference="ModelValue_58"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_87" name="Disso. from PE" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_87">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043280" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043624" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_41" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_40" stoichiometry="1"/>
          <Product metabolite="Metabolite_25" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_483" name="kdiesp" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_130">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_855">
              <SourceParameter reference="Metabolite_41"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_865">
              <SourceParameter reference="ModelValue_84"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_88" name="DNA synthesis" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_88">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0000082" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006261" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_39" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_21" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_19" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_482" name="eorib2" value="1"/>
          <Constant key="Parameter_481" name="eorib5" value="1"/>
          <Constant key="Parameter_480" name="ksori" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_131">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_447">
              <SourceParameter reference="Metabolite_19"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_873">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_806">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_1232">
              <SourceParameter reference="ModelValue_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_908">
              <SourceParameter reference="ModelValue_24"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_877">
              <SourceParameter reference="ModelValue_131"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_89" name="Negative regulation of DNA synthesis" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_89">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0008156" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_39" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_479" name="kdori" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_132">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_869">
              <SourceParameter reference="Metabolite_39"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_766">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_871">
              <SourceParameter reference="ModelValue_91"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_90" name="Budding" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_90">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0045782" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_23" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_24" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_478" name="ebudb5" value="1"/>
          <Constant key="Parameter_477" name="ebudn2" value="1"/>
          <Constant key="Parameter_476" name="ebudn3" value="1"/>
          <Constant key="Parameter_475" name="ksbud" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_133">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_778">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_893">
              <SourceParameter reference="Metabolite_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_833">
              <SourceParameter reference="Metabolite_24"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_895">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_851">
              <SourceParameter reference="ModelValue_6"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_897">
              <SourceParameter reference="ModelValue_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_637">
              <SourceParameter reference="ModelValue_8"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_899">
              <SourceParameter reference="ModelValue_121"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_91" name="Negative regulation of Cell budding" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_91">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0045781" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_474" name="kdbud" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_134">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_890">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_923">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_889">
              <SourceParameter reference="ModelValue_80"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_92" name="Spindle formation" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_92">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051225" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_49" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_19" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_473" name="Jspn" value="1"/>
          <Constant key="Parameter_472" name="ksspn" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_135">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_800">
              <SourceParameter reference="Metabolite_19"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_448">
              <SourceParameter reference="ModelValue_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_864">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_913">
              <SourceParameter reference="ModelValue_134"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_93" name="Spindle disassembly" reversible="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_93">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0051228" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_49" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_471" name="kdspn" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_136">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_870">
              <SourceParameter reference="Metabolite_49"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_914">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_919">
              <SourceParameter reference="ModelValue_94"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfEvents>
      <Event key="Event_0" name="reset ORI" order="1">
        <TriggerExpression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;+&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB5],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;-&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[KEZ2],Reference=Value&gt; lt 0
        </TriggerExpression>
        <ListOfAssignments>
          <Assignment targetKey="Metabolite_39">
            <Expression>
              0/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
        </ListOfAssignments>
      </Event>
      <Event key="Event_1" name="start DNA synthesis" order="2">
        <TriggerExpression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[ORI],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;-1 gt 0
        </TriggerExpression>
        <ListOfAssignments>
          <Assignment targetKey="Metabolite_33">
            <Expression>
              &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[mad2h],Reference=Value&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
          <Assignment targetKey="Metabolite_1">
            <Expression>
              &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[bub2h],Reference=Value&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
        </ListOfAssignments>
      </Event>
      <Event key="Event_2" name="spindle checkpoint" order="3">
        <TriggerExpression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[SPN],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;-1 gt 0
        </TriggerExpression>
        <ListOfAssignments>
          <Assignment targetKey="Metabolite_33">
            <Expression>
              &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[mad2l],Reference=Value&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
          <Assignment targetKey="Metabolite_32">
            <Expression>
              &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[lte1h],Reference=Value&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
          <Assignment targetKey="Metabolite_1">
            <Expression>
              &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[bub2l],Reference=Value&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
        </ListOfAssignments>
      </Event>
      <Event key="Event_3" name="cell division" order="4">
        <TriggerExpression>
          &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB2],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;-&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[KEZ],Reference=Value&gt; lt 0
        </TriggerExpression>
        <ListOfAssignments>
          <Assignment targetKey="Metabolite_34">
            <Expression>
              &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[F],Reference=Value&gt;*(&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[MASS],Reference=ParticleNumber&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[amount to particle factor],Reference=Value&gt;)/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
          <Assignment targetKey="Metabolite_32">
            <Expression>
              &lt;CN=Root,Model=Chen2004_CellCycle,Vector=Values[lte1l],Reference=Value&gt;/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
          <Assignment targetKey="Metabolite_2">
            <Expression>
              0/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
          <Assignment targetKey="Metabolite_49">
            <Expression>
              0/&lt;CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Reference=Volume&gt;
            </Expression>
          </Assignment>
        </ListOfAssignments>
      </Event>
    </ListOfEvents>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_1"/>
      <StateTemplateVariable objectReference="Metabolite_13"/>
      <StateTemplateVariable objectReference="Metabolite_46"/>
      <StateTemplateVariable objectReference="Metabolite_7"/>
      <StateTemplateVariable objectReference="Metabolite_19"/>
      <StateTemplateVariable objectReference="Metabolite_21"/>
      <StateTemplateVariable objectReference="Metabolite_36"/>
      <StateTemplateVariable objectReference="Metabolite_44"/>
      <StateTemplateVariable objectReference="Metabolite_14"/>
      <StateTemplateVariable objectReference="Metabolite_47"/>
      <StateTemplateVariable objectReference="Metabolite_16"/>
      <StateTemplateVariable objectReference="Metabolite_40"/>
      <StateTemplateVariable objectReference="Metabolite_12"/>
      <StateTemplateVariable objectReference="Metabolite_50"/>
      <StateTemplateVariable objectReference="Metabolite_37"/>
      <StateTemplateVariable objectReference="Metabolite_4"/>
      <StateTemplateVariable objectReference="Metabolite_29"/>
      <StateTemplateVariable objectReference="Metabolite_6"/>
      <StateTemplateVariable objectReference="Metabolite_27"/>
      <StateTemplateVariable objectReference="Metabolite_3"/>
      <StateTemplateVariable objectReference="Metabolite_28"/>
      <StateTemplateVariable objectReference="Metabolite_23"/>
      <StateTemplateVariable objectReference="Metabolite_31"/>
      <StateTemplateVariable objectReference="Metabolite_39"/>
      <StateTemplateVariable objectReference="Metabolite_42"/>
      <StateTemplateVariable objectReference="Metabolite_9"/>
      <StateTemplateVariable objectReference="Metabolite_2"/>
      <StateTemplateVariable objectReference="Metabolite_49"/>
      <StateTemplateVariable objectReference="Metabolite_53"/>
      <StateTemplateVariable objectReference="Metabolite_11"/>
      <StateTemplateVariable objectReference="Metabolite_17"/>
      <StateTemplateVariable objectReference="Metabolite_51"/>
      <StateTemplateVariable objectReference="Metabolite_25"/>
      <StateTemplateVariable objectReference="Metabolite_43"/>
      <StateTemplateVariable objectReference="Metabolite_5"/>
      <StateTemplateVariable objectReference="Metabolite_26"/>
      <StateTemplateVariable objectReference="Metabolite_34"/>
      <StateTemplateVariable objectReference="Metabolite_0"/>
      <StateTemplateVariable objectReference="Metabolite_10"/>
      <StateTemplateVariable objectReference="Metabolite_24"/>
      <StateTemplateVariable objectReference="Metabolite_30"/>
      <StateTemplateVariable objectReference="Metabolite_35"/>
      <StateTemplateVariable objectReference="Metabolite_41"/>
      <StateTemplateVariable objectReference="Metabolite_45"/>
      <StateTemplateVariable objectReference="Metabolite_52"/>
      <StateTemplateVariable objectReference="ModelValue_144"/>
      <StateTemplateVariable objectReference="ModelValue_145"/>
      <StateTemplateVariable objectReference="ModelValue_146"/>
      <StateTemplateVariable objectReference="ModelValue_147"/>
      <StateTemplateVariable objectReference="ModelValue_148"/>
      <StateTemplateVariable objectReference="ModelValue_149"/>
      <StateTemplateVariable objectReference="ModelValue_150"/>
      <StateTemplateVariable objectReference="ModelValue_151"/>
      <StateTemplateVariable objectReference="ModelValue_152"/>
      <StateTemplateVariable objectReference="ModelValue_153"/>
      <StateTemplateVariable objectReference="ModelValue_154"/>
      <StateTemplateVariable objectReference="ModelValue_155"/>
      <StateTemplateVariable objectReference="ModelValue_156"/>
      <StateTemplateVariable objectReference="ModelValue_157"/>
      <StateTemplateVariable objectReference="ModelValue_158"/>
      <StateTemplateVariable objectReference="ModelValue_159"/>
      <StateTemplateVariable objectReference="ModelValue_160"/>
      <StateTemplateVariable objectReference="ModelValue_161"/>
      <StateTemplateVariable objectReference="Metabolite_8"/>
      <StateTemplateVariable objectReference="Metabolite_15"/>
      <StateTemplateVariable objectReference="Metabolite_18"/>
      <StateTemplateVariable objectReference="Metabolite_20"/>
      <StateTemplateVariable objectReference="Metabolite_22"/>
      <StateTemplateVariable objectReference="Metabolite_38"/>
      <StateTemplateVariable objectReference="Metabolite_48"/>
      <StateTemplateVariable objectReference="ModelValue_143"/>
      <StateTemplateVariable objectReference="ModelValue_162"/>
      <StateTemplateVariable objectReference="Metabolite_1"/>
      <StateTemplateVariable objectReference="Metabolite_32"/>
      <StateTemplateVariable objectReference="Metabolite_33"/>
      <StateTemplateVariable objectReference="ModelValue_0"/>
      <StateTemplateVariable objectReference="ModelValue_1"/>
      <StateTemplateVariable objectReference="ModelValue_2"/>
      <StateTemplateVariable objectReference="ModelValue_3"/>
      <StateTemplateVariable objectReference="ModelValue_4"/>
      <StateTemplateVariable objectReference="ModelValue_5"/>
      <StateTemplateVariable objectReference="ModelValue_6"/>
      <StateTemplateVariable objectReference="ModelValue_7"/>
      <StateTemplateVariable objectReference="ModelValue_8"/>
      <StateTemplateVariable objectReference="ModelValue_9"/>
      <StateTemplateVariable objectReference="ModelValue_10"/>
      <StateTemplateVariable objectReference="ModelValue_11"/>
      <StateTemplateVariable objectReference="ModelValue_12"/>
      <StateTemplateVariable objectReference="ModelValue_13"/>
      <StateTemplateVariable objectReference="ModelValue_14"/>
      <StateTemplateVariable objectReference="ModelValue_15"/>
      <StateTemplateVariable objectReference="ModelValue_16"/>
      <StateTemplateVariable objectReference="ModelValue_17"/>
      <StateTemplateVariable objectReference="ModelValue_18"/>
      <StateTemplateVariable objectReference="ModelValue_19"/>
      <StateTemplateVariable objectReference="ModelValue_20"/>
      <StateTemplateVariable objectReference="ModelValue_21"/>
      <StateTemplateVariable objectReference="ModelValue_22"/>
      <StateTemplateVariable objectReference="ModelValue_23"/>
      <StateTemplateVariable objectReference="ModelValue_24"/>
      <StateTemplateVariable objectReference="ModelValue_25"/>
      <StateTemplateVariable objectReference="ModelValue_26"/>
      <StateTemplateVariable objectReference="ModelValue_27"/>
      <StateTemplateVariable objectReference="ModelValue_28"/>
      <StateTemplateVariable objectReference="ModelValue_29"/>
      <StateTemplateVariable objectReference="ModelValue_30"/>
      <StateTemplateVariable objectReference="ModelValue_31"/>
      <StateTemplateVariable objectReference="ModelValue_32"/>
      <StateTemplateVariable objectReference="ModelValue_33"/>
      <StateTemplateVariable objectReference="ModelValue_34"/>
      <StateTemplateVariable objectReference="ModelValue_35"/>
      <StateTemplateVariable objectReference="ModelValue_36"/>
      <StateTemplateVariable objectReference="ModelValue_37"/>
      <StateTemplateVariable objectReference="ModelValue_38"/>
      <StateTemplateVariable objectReference="ModelValue_39"/>
      <StateTemplateVariable objectReference="ModelValue_40"/>
      <StateTemplateVariable objectReference="ModelValue_41"/>
      <StateTemplateVariable objectReference="ModelValue_42"/>
      <StateTemplateVariable objectReference="ModelValue_43"/>
      <StateTemplateVariable objectReference="ModelValue_44"/>
      <StateTemplateVariable objectReference="ModelValue_45"/>
      <StateTemplateVariable objectReference="ModelValue_46"/>
      <StateTemplateVariable objectReference="ModelValue_47"/>
      <StateTemplateVariable objectReference="ModelValue_48"/>
      <StateTemplateVariable objectReference="ModelValue_49"/>
      <StateTemplateVariable objectReference="ModelValue_50"/>
      <StateTemplateVariable objectReference="ModelValue_51"/>
      <StateTemplateVariable objectReference="ModelValue_52"/>
      <StateTemplateVariable objectReference="ModelValue_53"/>
      <StateTemplateVariable objectReference="ModelValue_54"/>
      <StateTemplateVariable objectReference="ModelValue_55"/>
      <StateTemplateVariable objectReference="ModelValue_56"/>
      <StateTemplateVariable objectReference="ModelValue_57"/>
      <StateTemplateVariable objectReference="ModelValue_58"/>
      <StateTemplateVariable objectReference="ModelValue_59"/>
      <StateTemplateVariable objectReference="ModelValue_60"/>
      <StateTemplateVariable objectReference="ModelValue_61"/>
      <StateTemplateVariable objectReference="ModelValue_62"/>
      <StateTemplateVariable objectReference="ModelValue_63"/>
      <StateTemplateVariable objectReference="ModelValue_64"/>
      <StateTemplateVariable objectReference="ModelValue_65"/>
      <StateTemplateVariable objectReference="ModelValue_66"/>
      <StateTemplateVariable objectReference="ModelValue_67"/>
      <StateTemplateVariable objectReference="ModelValue_68"/>
      <StateTemplateVariable objectReference="ModelValue_69"/>
      <StateTemplateVariable objectReference="ModelValue_70"/>
      <StateTemplateVariable objectReference="ModelValue_71"/>
      <StateTemplateVariable objectReference="ModelValue_72"/>
      <StateTemplateVariable objectReference="ModelValue_73"/>
      <StateTemplateVariable objectReference="ModelValue_74"/>
      <StateTemplateVariable objectReference="ModelValue_75"/>
      <StateTemplateVariable objectReference="ModelValue_76"/>
      <StateTemplateVariable objectReference="ModelValue_77"/>
      <StateTemplateVariable objectReference="ModelValue_78"/>
      <StateTemplateVariable objectReference="ModelValue_79"/>
      <StateTemplateVariable objectReference="ModelValue_80"/>
      <StateTemplateVariable objectReference="ModelValue_81"/>
      <StateTemplateVariable objectReference="ModelValue_82"/>
      <StateTemplateVariable objectReference="ModelValue_83"/>
      <StateTemplateVariable objectReference="ModelValue_84"/>
      <StateTemplateVariable objectReference="ModelValue_85"/>
      <StateTemplateVariable objectReference="ModelValue_86"/>
      <StateTemplateVariable objectReference="ModelValue_87"/>
      <StateTemplateVariable objectReference="ModelValue_88"/>
      <StateTemplateVariable objectReference="ModelValue_89"/>
      <StateTemplateVariable objectReference="ModelValue_90"/>
      <StateTemplateVariable objectReference="ModelValue_91"/>
      <StateTemplateVariable objectReference="ModelValue_92"/>
      <StateTemplateVariable objectReference="ModelValue_93"/>
      <StateTemplateVariable objectReference="ModelValue_94"/>
      <StateTemplateVariable objectReference="ModelValue_95"/>
      <StateTemplateVariable objectReference="ModelValue_96"/>
      <StateTemplateVariable objectReference="ModelValue_97"/>
      <StateTemplateVariable objectReference="ModelValue_98"/>
      <StateTemplateVariable objectReference="ModelValue_99"/>
      <StateTemplateVariable objectReference="ModelValue_100"/>
      <StateTemplateVariable objectReference="ModelValue_101"/>
      <StateTemplateVariable objectReference="ModelValue_102"/>
      <StateTemplateVariable objectReference="ModelValue_103"/>
      <StateTemplateVariable objectReference="ModelValue_104"/>
      <StateTemplateVariable objectReference="ModelValue_105"/>
      <StateTemplateVariable objectReference="ModelValue_106"/>
      <StateTemplateVariable objectReference="ModelValue_107"/>
      <StateTemplateVariable objectReference="ModelValue_108"/>
      <StateTemplateVariable objectReference="ModelValue_109"/>
      <StateTemplateVariable objectReference="ModelValue_110"/>
      <StateTemplateVariable objectReference="ModelValue_111"/>
      <StateTemplateVariable objectReference="ModelValue_112"/>
      <StateTemplateVariable objectReference="ModelValue_113"/>
      <StateTemplateVariable objectReference="ModelValue_114"/>
      <StateTemplateVariable objectReference="ModelValue_115"/>
      <StateTemplateVariable objectReference="ModelValue_116"/>
      <StateTemplateVariable objectReference="ModelValue_117"/>
      <StateTemplateVariable objectReference="ModelValue_118"/>
      <StateTemplateVariable objectReference="ModelValue_119"/>
      <StateTemplateVariable objectReference="ModelValue_120"/>
      <StateTemplateVariable objectReference="ModelValue_121"/>
      <StateTemplateVariable objectReference="ModelValue_122"/>
      <StateTemplateVariable objectReference="ModelValue_123"/>
      <StateTemplateVariable objectReference="ModelValue_124"/>
      <StateTemplateVariable objectReference="ModelValue_125"/>
      <StateTemplateVariable objectReference="ModelValue_126"/>
      <StateTemplateVariable objectReference="ModelValue_127"/>
      <StateTemplateVariable objectReference="ModelValue_128"/>
      <StateTemplateVariable objectReference="ModelValue_129"/>
      <StateTemplateVariable objectReference="ModelValue_130"/>
      <StateTemplateVariable objectReference="ModelValue_131"/>
      <StateTemplateVariable objectReference="ModelValue_132"/>
      <StateTemplateVariable objectReference="ModelValue_133"/>
      <StateTemplateVariable objectReference="ModelValue_134"/>
      <StateTemplateVariable objectReference="ModelValue_135"/>
      <StateTemplateVariable objectReference="ModelValue_136"/>
      <StateTemplateVariable objectReference="ModelValue_137"/>
      <StateTemplateVariable objectReference="ModelValue_138"/>
      <StateTemplateVariable objectReference="ModelValue_139"/>
      <StateTemplateVariable objectReference="ModelValue_140"/>
      <StateTemplateVariable objectReference="ModelValue_141"/>
      <StateTemplateVariable objectReference="ModelValue_142"/>
      <StateTemplateVariable objectReference="ModelValue_163"/>
      <StateTemplateVariable objectReference="Compartment_0"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 6.478619825700005e+22 1.377721443804e+22 2.820433838676002e+23 8.84789288962051e+22 3.119553606981002e+22 1.122828282675e+22 3.6132849e+23 9.3258883269e+21 3.8601927015e+21 5.603596643608505e+23 1.54239088098e+22 8.864857262225999e+23 5.721034425000003e+23 5.843109255346505e+23 1.44736148811e+22 4.7635139265e+19 4.142028923700005e+21 1.649693398227001e+22 1.435702622166e+23 4.360030446000005e+19 3.9295135723065e+22 6.112473622500004e+22 6.0221415e+23 7.418013678285006e+22 3.953734625419505e+23 5.10256049295e+21 1.806642450000001e+22 5.419927350000004e+23 2.675613379884e+23 4.185388342500005e+22 1.2044283e+22 1.8145495217895e+23 6.320478389909999e+23 4.220376984615007e+22 1.421574678207e+23 7.2628170696885e+23 3.921921217631791e+22 2.068406874580496e+23 4.031528126522287e+22 5.41089413775e+23 2.82443024144511e+23 4.2075919782105e+23 2.959123010097807e+21 6.022141499999959e+22 0.007701635339554948 0.08108736 0.4418440000000003 0.5908263458114359 1.775381600000001 0.2422695871203281 0.2663495285233923 0.3846752000000003 0.05168441222637602 0.4195370000000002 0.4871349532762005 0.8946186673169543 0.13607916 0.01469227000000002 0.09724769917563975 0.1119399691756398 1.873376000000001 1.873376000000001 1.2754197128586e+24 2.32857723830595e+23 4.548848068376852e+23 4.051772077968751e+23 7.763257028338508e+22 1.5889155373524e+24 2.220270830070901e+23 101.2184600756869 0.4586134093959288 1.2044283e+23 6.022141500000004e+22 6.0221415e+21 0.054 1 0.2 0.4 1 1 1 0.25 0.05 0.45 0.1 0.03 0.06 0.3 0.55 0.1 0.03 0.06 0.3 1.2 8 0.4 0.25 0.45 0.9 2 2 10 1 1 0.15 0.03 0.1 0.1 0.01 0.1 0.05 0.05 0.03 0.1 0.1 0.01 0.1 6 0.04 0.14 0.002 1 0.001 0.05 0.2 0.01 0.8 0.1 1 50 50 0.38 50 15 0.01 200 1 2 0.1 0.01 0.01 0.01 0.3 1 1 0.2 1 1 0.04 0.003 0.4 0.15 0.01 0.16 0.06 0.01 0.05 0.06 0.5 0.5 0.01 1 2 0.12 0.03 0.06 0.17 2 0.06 0.08 0.3 0.2 0.5 0.001 0.08 0.15 0.15 0.6 8 0.05 0.01 0.6 4 4 0.05 3 0.2 0.03 0.006 0.6 0.055 0.001 0.04 0.0008 0.005 0.2 0.012 0.12 0.01 0.024 0.12 0.004 0 0.15 0.08400000000000001 2 0 0.1 0.1 0.005 0.08 1 0.1 8 0.01 90 1 6.0221415e+23 1 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_2" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_0" target="" append="1"/>
      <Problem>
        <Parameter name="JacobianRequested" type="bool" value="1"/>
        <Parameter name="StabilityAnalysisRequested" type="bool" value="1"/>
      </Problem>
      <Method name="Enhanced Newton" type="EnhancedNewton">
        <Parameter name="Resolution" type="unsignedFloat" value="1e-09"/>
        <Parameter name="Derivation Factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Use Newton" type="bool" value="1"/>
        <Parameter name="Use Integration" type="bool" value="1"/>
        <Parameter name="Use Back Integration" type="bool" value="1"/>
        <Parameter name="Accept Negative Concentrations" type="bool" value="0"/>
        <Parameter name="Iteration Limit" type="unsignedInteger" value="50"/>
        <Parameter name="Maximum duration for forward integration" type="unsignedFloat" value="1e+09"/>
        <Parameter name="Maximum duration for backward integration" type="unsignedFloat" value="1e+06"/>
      </Method>
    </Task>
    <Task key="Task_3" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="2"/>
        <Parameter name="Duration" type="float" value="200"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_4" name="Scan" type="scan" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="1"/>
        <ParameterGroup name="ScanItems">
        </ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="1"/>
        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
      </Problem>
      <Method name="Scan Framework" type="ScanFramework">
      </Method>
    </Task>
    <Task key="Task_5" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_1" target="" append="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_6" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_2" target="" append="1"/>
      <Problem>
        <Parameter name="Subtask" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <ParameterText name="ObjectiveExpression" type="expression">
          
        </ParameterText>
        <Parameter name="Maximize" type="bool" value="0"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
      </Problem>
      <Method name="Random Search" type="RandomSearch">
        <Parameter name="Number of Iterations" type="unsignedInteger" value="100000"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_7" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
      <Report reference="Report_3" target="" append="1"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <ParameterGroup name="Experiment Set">
        </ParameterGroup>
      </Problem>
      <Method name="Evolutionary Programming" type="EvolutionaryProgram">
        <Parameter name="Number of Generations" type="unsignedInteger" value="200"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_8" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_4" target="" append="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_2"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-09"/>
      </Method>
    </Task>
    <Task key="Task_9" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_5" target="" append="1"/>
      <Problem>
        <Parameter name="ExponentNumber" type="unsignedInteger" value="3"/>
        <Parameter name="DivergenceRequested" type="bool" value="1"/>
        <Parameter name="TransientTime" type="float" value="0"/>
      </Problem>
      <Method name="Wolf Method" type="WolfMethod">
        <Parameter name="Orthonormalization Interval" type="unsignedFloat" value="1"/>
        <Parameter name="Overall time" type="unsignedFloat" value="1000"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_11" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_6" target="" append="1"/>
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="1"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
      </Problem>
      <Method name="ILDM (LSODA,Deuflhard)" type="TimeScaleSeparation(ILDM,Deuflhard)">
        <Parameter name="Deuflhard Tolerance" type="unsignedFloat" value="1e-06"/>
      </Method>
    </Task>
    <Task key="Task_1" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
      <Report reference="Report_7" target="" append="1"/>
      <Problem>
        <Parameter name="SubtaskType" type="unsignedInteger" value="1"/>
        <ParameterGroup name="TargetFunctions">
          <Parameter name="SingleObject" type="cn" value=""/>
          <Parameter name="ObjectListType" type="unsignedInteger" value="7"/>
        </ParameterGroup>
        <ParameterGroup name="ListOfVariables">
          <ParameterGroup name="Variables">
            <Parameter name="SingleObject" type="cn" value=""/>
            <Parameter name="ObjectListType" type="unsignedInteger" value="41"/>
          </ParameterGroup>
        </ParameterGroup>
      </Problem>
      <Method name="Sensitivities Method" type="SensitivitiesMethod">
        <Parameter name="Delta factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Delta minimum" type="unsignedFloat" value="1e-12"/>
      </Method>
    </Task>
    <Task key="Task_0" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_0" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_1" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_2" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_3" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_4" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_5" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_6" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_7" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
      </Footer>
    </Report>
  </ListOfReports>
  <ListOfPlots>
    <PlotSpecification name="paper" type="Plot2D" active="1">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="[BUD]|Time" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[BUD],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[CDH1]|Time" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CDH1],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[CLN2]|Time" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLN2],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[MASS]|Time" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[MASS],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[SIC1T]|Time" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[SIC1T],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[CLB5T]|Time" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[CLB5T],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[ORI]|Time" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[ORI],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[SBF]|Time" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Chen2004_CellCycle,Vector=Compartments[cell],Vector=Metabolites[SBF],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
  </ListOfPlots>
  <GUI>
  </GUI>
  <SBMLReference file="BIOMD0000000056.xml">
    <SBMLMap SBMLid="Activation_of_CDC20" COPASIkey="Reaction_53"/>
    <SBMLMap SBMLid="Activation_of_IEP" COPASIkey="Reaction_48"/>
    <SBMLMap SBMLid="Activation_of_SWI5" COPASIkey="Reaction_46"/>
    <SBMLMap SBMLid="Assoc_of_CLB2_and_SIC1" COPASIkey="Reaction_11"/>
    <SBMLMap SBMLid="Assoc_of_CLB5_and_SIC1" COPASIkey="Reaction_13"/>
    <SBMLMap SBMLid="Assoc_with_ESP1_to_form_PE" COPASIkey="Reaction_86"/>
    <SBMLMap SBMLid="Assoc_with_NET1P_to_form_RENTP" COPASIkey="Reaction_64"/>
    <SBMLMap SBMLid="Assoc_with_NET1_to_form_RENT" COPASIkey="Reaction_62"/>
    <SBMLMap SBMLid="BCK2" COPASIkey="Metabolite_0"/>
    <SBMLMap SBMLid="BUB2" COPASIkey="Metabolite_1"/>
    <SBMLMap SBMLid="BUD" COPASIkey="Metabolite_2"/>
    <SBMLMap SBMLid="Budding" COPASIkey="Reaction_90"/>
    <SBMLMap SBMLid="C0" COPASIkey="ModelValue_3"/>
    <SBMLMap SBMLid="C2" COPASIkey="Metabolite_3"/>
    <SBMLMap SBMLid="C2P" COPASIkey="Metabolite_4"/>
    <SBMLMap SBMLid="C5" COPASIkey="Metabolite_5"/>
    <SBMLMap SBMLid="C5P" COPASIkey="Metabolite_6"/>
    <SBMLMap SBMLid="CDC14" COPASIkey="Metabolite_7"/>
    <SBMLMap SBMLid="CDC14T" COPASIkey="Metabolite_8"/>
    <SBMLMap SBMLid="CDC14_degradation" COPASIkey="Reaction_61"/>
    <SBMLMap SBMLid="CDC14_synthesis" COPASIkey="Reaction_60"/>
    <SBMLMap SBMLid="CDC15" COPASIkey="Metabolite_9"/>
    <SBMLMap SBMLid="CDC15T" COPASIkey="ModelValue_4"/>
    <SBMLMap SBMLid="CDC15_activation" COPASIkey="Reaction_79"/>
    <SBMLMap SBMLid="CDC15i" COPASIkey="Metabolite_10"/>
    <SBMLMap SBMLid="CDC20" COPASIkey="Metabolite_11"/>
    <SBMLMap SBMLid="CDC20i" COPASIkey="Metabolite_12"/>
    <SBMLMap SBMLid="CDC6" COPASIkey="Metabolite_13"/>
    <SBMLMap SBMLid="CDC6P" COPASIkey="Metabolite_14"/>
    <SBMLMap SBMLid="CDC6T" COPASIkey="Metabolite_15"/>
    <SBMLMap SBMLid="CDC6_degradation_in_F2P" COPASIkey="Reaction_39"/>
    <SBMLMap SBMLid="CDC6_degradation_in_F5P" COPASIkey="Reaction_40"/>
    <SBMLMap SBMLid="CDC6_synthesis" COPASIkey="Reaction_25"/>
    <SBMLMap SBMLid="CDH1" COPASIkey="Metabolite_16"/>
    <SBMLMap SBMLid="CDH1_degradation" COPASIkey="Reaction_56"/>
    <SBMLMap SBMLid="CDH1_synthesis" COPASIkey="Reaction_55"/>
    <SBMLMap SBMLid="CDH1i" COPASIkey="Metabolite_17"/>
    <SBMLMap SBMLid="CDH1i_activation" COPASIkey="Reaction_58"/>
    <SBMLMap SBMLid="CDH1i_degradation" COPASIkey="Reaction_57"/>
    <SBMLMap SBMLid="CKIT" COPASIkey="Metabolite_18"/>
    <SBMLMap SBMLid="CLB2" COPASIkey="Metabolite_19"/>
    <SBMLMap SBMLid="CLB2CDC6_complex_formation" COPASIkey="Reaction_29"/>
    <SBMLMap SBMLid="CLB2CDC6_dissociation" COPASIkey="Reaction_30"/>
    <SBMLMap SBMLid="CLB2T" COPASIkey="Metabolite_20"/>
    <SBMLMap SBMLid="CLB2_degradation_in_F2" COPASIkey="Reaction_37"/>
    <SBMLMap SBMLid="CLB2_degradation_in_F2P" COPASIkey="Reaction_41"/>
    <SBMLMap SBMLid="CLB5" COPASIkey="Metabolite_21"/>
    <SBMLMap SBMLid="CLB5CDC6_complex_formation" COPASIkey="Reaction_31"/>
    <SBMLMap SBMLid="CLB5CDC6_dissociation" COPASIkey="Reaction_32"/>
    <SBMLMap SBMLid="CLB5T" COPASIkey="Metabolite_22"/>
    <SBMLMap SBMLid="CLB5_degradation_in_F5" COPASIkey="Reaction_38"/>
    <SBMLMap SBMLid="CLB5_degradation_in_F5P" COPASIkey="Reaction_42"/>
    <SBMLMap SBMLid="CLN2" COPASIkey="Metabolite_23"/>
    <SBMLMap SBMLid="CLN3" COPASIkey="Metabolite_24"/>
    <SBMLMap SBMLid="D" COPASIkey="ModelValue_143"/>
    <SBMLMap SBMLid="DNA_synthesis" COPASIkey="Reaction_88"/>
    <SBMLMap SBMLid="Degradation_of_CDC14_in_RENT" COPASIkey="Reaction_75"/>
    <SBMLMap SBMLid="Degradation_of_CDC14_in_RENTP" COPASIkey="Reaction_76"/>
    <SBMLMap SBMLid="Degradation_of_CDC6P" COPASIkey="Reaction_28"/>
    <SBMLMap SBMLid="Degradation_of_CLB2" COPASIkey="Reaction_4"/>
    <SBMLMap SBMLid="Degradation_of_CLB2_in_C2" COPASIkey="Reaction_19"/>
    <SBMLMap SBMLid="Degradation_of_CLB2_in_C2P" COPASIkey="Reaction_23"/>
    <SBMLMap SBMLid="Degradation_of_CLB5" COPASIkey="Reaction_6"/>
    <SBMLMap SBMLid="Degradation_of_CLB5_in_C5" COPASIkey="Reaction_20"/>
    <SBMLMap SBMLid="Degradation_of_CLB5_in_C5P" COPASIkey="Reaction_24"/>
    <SBMLMap SBMLid="Degradation_of_CLN2" COPASIkey="Reaction_2"/>
    <SBMLMap SBMLid="Degradation_of_NET1P_in_RENTP" COPASIkey="Reaction_74"/>
    <SBMLMap SBMLid="Degradation_of_NET1_in_RENT" COPASIkey="Reaction_73"/>
    <SBMLMap SBMLid="Degradation_of_PDS1_in_PE" COPASIkey="Reaction_85"/>
    <SBMLMap SBMLid="Degradation_of_SIC1P_in_C5P_" COPASIkey="Reaction_22"/>
    <SBMLMap SBMLid="Degradation_of_SIC1_in_C2P" COPASIkey="Reaction_21"/>
    <SBMLMap SBMLid="Degradation_of_SWI5" COPASIkey="Reaction_44"/>
    <SBMLMap SBMLid="Degradation_of_SWI5P" COPASIkey="Reaction_45"/>
    <SBMLMap SBMLid="Degradation_of_active_CDC20" COPASIkey="Reaction_52"/>
    <SBMLMap SBMLid="Degradation_of_inactiveCDC20" COPASIkey="Reaction_51"/>
    <SBMLMap SBMLid="Dephosphorylation_of_C2P" COPASIkey="Reaction_16"/>
    <SBMLMap SBMLid="Dephosphorylation_of_C5P" COPASIkey="Reaction_18"/>
    <SBMLMap SBMLid="Dephosphorylation_of_CDC6" COPASIkey="Reaction_27"/>
    <SBMLMap SBMLid="Dephosphorylation_of_SIC1" COPASIkey="Reaction_9"/>
    <SBMLMap SBMLid="Disso_from_PE" COPASIkey="Reaction_87"/>
    <SBMLMap SBMLid="Dissoc_from_RENP" COPASIkey="Reaction_65"/>
    <SBMLMap SBMLid="Dissoc_from_RENT" COPASIkey="Reaction_63"/>
    <SBMLMap SBMLid="Dissoc_of_CLB2SIC1_complex" COPASIkey="Reaction_12"/>
    <SBMLMap SBMLid="Dissoc_of_CLB5SIC1" COPASIkey="Reaction_14"/>
    <SBMLMap SBMLid="Dn3" COPASIkey="ModelValue_5"/>
    <SBMLMap SBMLid="ESP1" COPASIkey="Metabolite_25"/>
    <SBMLMap SBMLid="ESP1T" COPASIkey="ModelValue_28"/>
    <SBMLMap SBMLid="F" COPASIkey="ModelValue_162"/>
    <SBMLMap SBMLid="F2" COPASIkey="Metabolite_26"/>
    <SBMLMap SBMLid="F2P" COPASIkey="Metabolite_27"/>
    <SBMLMap SBMLid="F2P_dephosphorylation" COPASIkey="Reaction_34"/>
    <SBMLMap SBMLid="F2_phosphorylation" COPASIkey="Reaction_33"/>
    <SBMLMap SBMLid="F5" COPASIkey="Metabolite_28"/>
    <SBMLMap SBMLid="F5P" COPASIkey="Metabolite_29"/>
    <SBMLMap SBMLid="F5P_dephosphorylation" COPASIkey="Reaction_36"/>
    <SBMLMap SBMLid="F5_phosphorylation" COPASIkey="Reaction_35"/>
    <SBMLMap SBMLid="Fast_Degradation_of_SIC1P" COPASIkey="Reaction_10"/>
    <SBMLMap SBMLid="GK_219" COPASIkey="Function_331"/>
    <SBMLMap SBMLid="Growth" COPASIkey="Reaction_0"/>
    <SBMLMap SBMLid="IE" COPASIkey="Metabolite_30"/>
    <SBMLMap SBMLid="IEP" COPASIkey="Metabolite_31"/>
    <SBMLMap SBMLid="IET" COPASIkey="ModelValue_29"/>
    <SBMLMap SBMLid="Inactivation_1" COPASIkey="Reaction_49"/>
    <SBMLMap SBMLid="Inactivation_2" COPASIkey="Reaction_54"/>
    <SBMLMap SBMLid="Inactivation_3" COPASIkey="Reaction_59"/>
    <SBMLMap SBMLid="Inactivation_of_SWI5" COPASIkey="Reaction_47"/>
    <SBMLMap SBMLid="J20ppx" COPASIkey="ModelValue_30"/>
    <SBMLMap SBMLid="Jacdh" COPASIkey="ModelValue_31"/>
    <SBMLMap SBMLid="Jaiep" COPASIkey="ModelValue_32"/>
    <SBMLMap SBMLid="Jamcm" COPASIkey="ModelValue_33"/>
    <SBMLMap SBMLid="Jasbf" COPASIkey="ModelValue_34"/>
    <SBMLMap SBMLid="Jatem" COPASIkey="ModelValue_35"/>
    <SBMLMap SBMLid="Jd2c1" COPASIkey="ModelValue_36"/>
    <SBMLMap SBMLid="Jd2f6" COPASIkey="ModelValue_37"/>
    <SBMLMap SBMLid="Jicdh" COPASIkey="ModelValue_38"/>
    <SBMLMap SBMLid="Jiiep" COPASIkey="ModelValue_39"/>
    <SBMLMap SBMLid="Jimcm" COPASIkey="ModelValue_40"/>
    <SBMLMap SBMLid="Jisbf" COPASIkey="ModelValue_41"/>
    <SBMLMap SBMLid="Jitem" COPASIkey="ModelValue_42"/>
    <SBMLMap SBMLid="Jn3" COPASIkey="ModelValue_43"/>
    <SBMLMap SBMLid="Jpds" COPASIkey="ModelValue_44"/>
    <SBMLMap SBMLid="Jspn" COPASIkey="ModelValue_45"/>
    <SBMLMap SBMLid="KEZ" COPASIkey="ModelValue_96"/>
    <SBMLMap SBMLid="KEZ2" COPASIkey="ModelValue_97"/>
    <SBMLMap SBMLid="LTE1" COPASIkey="Metabolite_32"/>
    <SBMLMap SBMLid="MAD2" COPASIkey="Metabolite_33"/>
    <SBMLMap SBMLid="MASS" COPASIkey="Metabolite_34"/>
    <SBMLMap SBMLid="MCM1" COPASIkey="Metabolite_35"/>
    <SBMLMap SBMLid="Mass_Action_1_222" COPASIkey="Function_351"/>
    <SBMLMap SBMLid="Mass_Action_2_221" COPASIkey="Function_247"/>
    <SBMLMap SBMLid="MichaelisMenten_220" COPASIkey="Function_37"/>
    <SBMLMap SBMLid="NET1" COPASIkey="Metabolite_36"/>
    <SBMLMap SBMLid="NET1P" COPASIkey="Metabolite_37"/>
    <SBMLMap SBMLid="NET1T" COPASIkey="Metabolite_38"/>
    <SBMLMap SBMLid="NET1_phosphorylation" COPASIkey="Reaction_69"/>
    <SBMLMap SBMLid="Negative_regulation_of_Cell_budding" COPASIkey="Reaction_91"/>
    <SBMLMap SBMLid="Negative_regulation_of_DNA_synthesis" COPASIkey="Reaction_89"/>
    <SBMLMap SBMLid="Net1P_degradation" COPASIkey="Reaction_68"/>
    <SBMLMap SBMLid="Net1_degradation" COPASIkey="Reaction_67"/>
    <SBMLMap SBMLid="Net1_synthesis" COPASIkey="Reaction_66"/>
    <SBMLMap SBMLid="ORI" COPASIkey="Metabolite_39"/>
    <SBMLMap SBMLid="PDS1" COPASIkey="Metabolite_40"/>
    <SBMLMap SBMLid="PDS1_synthesis" COPASIkey="Reaction_83"/>
    <SBMLMap SBMLid="PE" COPASIkey="Metabolite_41"/>
    <SBMLMap SBMLid="PPX" COPASIkey="Metabolite_42"/>
    <SBMLMap SBMLid="PPX_synthesis" COPASIkey="Reaction_81"/>
    <SBMLMap SBMLid="Phosphorylation_of_C2" COPASIkey="Reaction_15"/>
    <SBMLMap SBMLid="Phosphorylation_of_C5" COPASIkey="Reaction_17"/>
    <SBMLMap SBMLid="Phosphorylation_of_CDC6" COPASIkey="Reaction_26"/>
    <SBMLMap SBMLid="Phosphorylation_of_SIC1" COPASIkey="Reaction_8"/>
    <SBMLMap SBMLid="RENT" COPASIkey="Metabolite_43"/>
    <SBMLMap SBMLid="RENTP" COPASIkey="Metabolite_44"/>
    <SBMLMap SBMLid="RENT_phosphorylation" COPASIkey="Reaction_71"/>
    <SBMLMap SBMLid="SBF" COPASIkey="Metabolite_45"/>
    <SBMLMap SBMLid="SIC1" COPASIkey="Metabolite_46"/>
    <SBMLMap SBMLid="SIC1P" COPASIkey="Metabolite_47"/>
    <SBMLMap SBMLid="SIC1T" COPASIkey="Metabolite_48"/>
    <SBMLMap SBMLid="SPN" COPASIkey="Metabolite_49"/>
    <SBMLMap SBMLid="SWI5" COPASIkey="Metabolite_50"/>
    <SBMLMap SBMLid="SWI5P" COPASIkey="Metabolite_51"/>
    <SBMLMap SBMLid="Spindle_disassembly" COPASIkey="Reaction_93"/>
    <SBMLMap SBMLid="Spindle_formation" COPASIkey="Reaction_92"/>
    <SBMLMap SBMLid="Synthesis_of_CLB2" COPASIkey="Reaction_3"/>
    <SBMLMap SBMLid="Synthesis_of_CLB5" COPASIkey="Reaction_5"/>
    <SBMLMap SBMLid="Synthesis_of_CLN2" COPASIkey="Reaction_1"/>
    <SBMLMap SBMLid="Synthesis_of_SIC1" COPASIkey="Reaction_7"/>
    <SBMLMap SBMLid="Synthesis_of_SWI5" COPASIkey="Reaction_43"/>
    <SBMLMap SBMLid="Synthesis_of_inactive_CDC20" COPASIkey="Reaction_50"/>
    <SBMLMap SBMLid="TEM1GDP" COPASIkey="Metabolite_52"/>
    <SBMLMap SBMLid="TEM1GTP" COPASIkey="Metabolite_53"/>
    <SBMLMap SBMLid="TEM1T" COPASIkey="ModelValue_142"/>
    <SBMLMap SBMLid="TEM1_activation" COPASIkey="Reaction_77"/>
    <SBMLMap SBMLid="Vacdh" COPASIkey="ModelValue_151"/>
    <SBMLMap SBMLid="Vaiep" COPASIkey="ModelValue_157"/>
    <SBMLMap SBMLid="Vasbf" COPASIkey="ModelValue_147"/>
    <SBMLMap SBMLid="Vd2c1" COPASIkey="ModelValue_158"/>
    <SBMLMap SBMLid="Vd2f6" COPASIkey="ModelValue_159"/>
    <SBMLMap SBMLid="Vdb2" COPASIkey="ModelValue_146"/>
    <SBMLMap SBMLid="Vdb5" COPASIkey="ModelValue_145"/>
    <SBMLMap SBMLid="Vdpds" COPASIkey="ModelValue_156"/>
    <SBMLMap SBMLid="Vdppx" COPASIkey="ModelValue_155"/>
    <SBMLMap SBMLid="Vicdh" COPASIkey="ModelValue_152"/>
    <SBMLMap SBMLid="Visbf" COPASIkey="ModelValue_148"/>
    <SBMLMap SBMLid="Vkpc1" COPASIkey="ModelValue_149"/>
    <SBMLMap SBMLid="Vkpf6" COPASIkey="ModelValue_150"/>
    <SBMLMap SBMLid="Vkpnet" COPASIkey="ModelValue_154"/>
    <SBMLMap SBMLid="Vppc1" COPASIkey="ModelValue_160"/>
    <SBMLMap SBMLid="Vppf6" COPASIkey="ModelValue_161"/>
    <SBMLMap SBMLid="Vppnet" COPASIkey="ModelValue_153"/>
    <SBMLMap SBMLid="b0" COPASIkey="ModelValue_0"/>
    <SBMLMap SBMLid="bub2h" COPASIkey="ModelValue_1"/>
    <SBMLMap SBMLid="bub2l" COPASIkey="ModelValue_2"/>
    <SBMLMap SBMLid="cell" COPASIkey="Compartment_0"/>
    <SBMLMap SBMLid="degradation_1" COPASIkey="Reaction_82"/>
    <SBMLMap SBMLid="degradation_2" COPASIkey="Reaction_84"/>
    <SBMLMap SBMLid="dephosphorylation_1" COPASIkey="Reaction_70"/>
    <SBMLMap SBMLid="dephosphorylation_2" COPASIkey="Reaction_72"/>
    <SBMLMap SBMLid="ebudb5" COPASIkey="ModelValue_6"/>
    <SBMLMap SBMLid="ebudn2" COPASIkey="ModelValue_7"/>
    <SBMLMap SBMLid="ebudn3" COPASIkey="ModelValue_8"/>
    <SBMLMap SBMLid="ec1b2" COPASIkey="ModelValue_9"/>
    <SBMLMap SBMLid="ec1b5" COPASIkey="ModelValue_10"/>
    <SBMLMap SBMLid="ec1k2" COPASIkey="ModelValue_11"/>
    <SBMLMap SBMLid="ec1n2" COPASIkey="ModelValue_12"/>
    <SBMLMap SBMLid="ec1n3" COPASIkey="ModelValue_13"/>
    <SBMLMap SBMLid="ef6b2" COPASIkey="ModelValue_14"/>
    <SBMLMap SBMLid="ef6b5" COPASIkey="ModelValue_15"/>
    <SBMLMap SBMLid="ef6k2" COPASIkey="ModelValue_16"/>
    <SBMLMap SBMLid="ef6n2" COPASIkey="ModelValue_17"/>
    <SBMLMap SBMLid="ef6n3" COPASIkey="ModelValue_18"/>
    <SBMLMap SBMLid="eicdhb2" COPASIkey="ModelValue_19"/>
    <SBMLMap SBMLid="eicdhb5" COPASIkey="ModelValue_20"/>
    <SBMLMap SBMLid="eicdhn2" COPASIkey="ModelValue_21"/>
    <SBMLMap SBMLid="eicdhn3" COPASIkey="ModelValue_22"/>
    <SBMLMap SBMLid="eorib2" COPASIkey="ModelValue_23"/>
    <SBMLMap SBMLid="eorib5" COPASIkey="ModelValue_24"/>
    <SBMLMap SBMLid="esbfb5" COPASIkey="ModelValue_25"/>
    <SBMLMap SBMLid="esbfn2" COPASIkey="ModelValue_26"/>
    <SBMLMap SBMLid="esbfn3" COPASIkey="ModelValue_27"/>
    <SBMLMap SBMLid="inactivation_1" COPASIkey="Reaction_78"/>
    <SBMLMap SBMLid="inactivation_2" COPASIkey="Reaction_80"/>
    <SBMLMap SBMLid="ka15_p" COPASIkey="ModelValue_46"/>
    <SBMLMap SBMLid="ka15_p_p" COPASIkey="ModelValue_47"/>
    <SBMLMap SBMLid="ka15p" COPASIkey="ModelValue_48"/>
    <SBMLMap SBMLid="ka20_p" COPASIkey="ModelValue_49"/>
    <SBMLMap SBMLid="ka20_p_p" COPASIkey="ModelValue_50"/>
    <SBMLMap SBMLid="kacdh_p" COPASIkey="ModelValue_51"/>
    <SBMLMap SBMLid="kacdh_p_p" COPASIkey="ModelValue_52"/>
    <SBMLMap SBMLid="kaiep" COPASIkey="ModelValue_53"/>
    <SBMLMap SBMLid="kamcm" COPASIkey="ModelValue_54"/>
    <SBMLMap SBMLid="kasb2" COPASIkey="ModelValue_55"/>
    <SBMLMap SBMLid="kasb5" COPASIkey="ModelValue_56"/>
    <SBMLMap SBMLid="kasbf" COPASIkey="ModelValue_57"/>
    <SBMLMap SBMLid="kasesp" COPASIkey="ModelValue_58"/>
    <SBMLMap SBMLid="kasf2" COPASIkey="ModelValue_59"/>
    <SBMLMap SBMLid="kasf5" COPASIkey="ModelValue_60"/>
    <SBMLMap SBMLid="kasrent" COPASIkey="ModelValue_61"/>
    <SBMLMap SBMLid="kasrentp" COPASIkey="ModelValue_62"/>
    <SBMLMap SBMLid="kaswi" COPASIkey="ModelValue_63"/>
    <SBMLMap SBMLid="kd14" COPASIkey="ModelValue_64"/>
    <SBMLMap SBMLid="kd1c1" COPASIkey="ModelValue_65"/>
    <SBMLMap SBMLid="kd1f6" COPASIkey="ModelValue_66"/>
    <SBMLMap SBMLid="kd1pds_p" COPASIkey="ModelValue_67"/>
    <SBMLMap SBMLid="kd20" COPASIkey="ModelValue_68"/>
    <SBMLMap SBMLid="kd2c1" COPASIkey="ModelValue_69"/>
    <SBMLMap SBMLid="kd2f6" COPASIkey="ModelValue_70"/>
    <SBMLMap SBMLid="kd2pds_p_p" COPASIkey="ModelValue_71"/>
    <SBMLMap SBMLid="kd3c1" COPASIkey="ModelValue_72"/>
    <SBMLMap SBMLid="kd3f6" COPASIkey="ModelValue_73"/>
    <SBMLMap SBMLid="kd3pds_p_p" COPASIkey="ModelValue_74"/>
    <SBMLMap SBMLid="kdb2_p" COPASIkey="ModelValue_75"/>
    <SBMLMap SBMLid="kdb2_p_p" COPASIkey="ModelValue_76"/>
    <SBMLMap SBMLid="kdb2p" COPASIkey="ModelValue_77"/>
    <SBMLMap SBMLid="kdb5_p" COPASIkey="ModelValue_78"/>
    <SBMLMap SBMLid="kdb5_p_p" COPASIkey="ModelValue_79"/>
    <SBMLMap SBMLid="kdbud" COPASIkey="ModelValue_80"/>
    <SBMLMap SBMLid="kdcdh" COPASIkey="ModelValue_81"/>
    <SBMLMap SBMLid="kdib2" COPASIkey="ModelValue_82"/>
    <SBMLMap SBMLid="kdib5" COPASIkey="ModelValue_83"/>
    <SBMLMap SBMLid="kdiesp" COPASIkey="ModelValue_84"/>
    <SBMLMap SBMLid="kdif2" COPASIkey="ModelValue_85"/>
    <SBMLMap SBMLid="kdif5" COPASIkey="ModelValue_86"/>
    <SBMLMap SBMLid="kdirent" COPASIkey="ModelValue_87"/>
    <SBMLMap SBMLid="kdirentp" COPASIkey="ModelValue_88"/>
    <SBMLMap SBMLid="kdn2" COPASIkey="ModelValue_89"/>
    <SBMLMap SBMLid="kdnet" COPASIkey="ModelValue_90"/>
    <SBMLMap SBMLid="kdori" COPASIkey="ModelValue_91"/>
    <SBMLMap SBMLid="kdppx_p" COPASIkey="ModelValue_92"/>
    <SBMLMap SBMLid="kdppx_p_p" COPASIkey="ModelValue_93"/>
    <SBMLMap SBMLid="kdspn" COPASIkey="ModelValue_94"/>
    <SBMLMap SBMLid="kdswi" COPASIkey="ModelValue_95"/>
    <SBMLMap SBMLid="ki15" COPASIkey="ModelValue_98"/>
    <SBMLMap SBMLid="kicdh_p" COPASIkey="ModelValue_99"/>
    <SBMLMap SBMLid="kicdh_p_p" COPASIkey="ModelValue_100"/>
    <SBMLMap SBMLid="kiiep" COPASIkey="ModelValue_101"/>
    <SBMLMap SBMLid="kimcm" COPASIkey="ModelValue_102"/>
    <SBMLMap SBMLid="kisbf_p" COPASIkey="ModelValue_103"/>
    <SBMLMap SBMLid="kisbf_p_p" COPASIkey="ModelValue_104"/>
    <SBMLMap SBMLid="kiswi" COPASIkey="ModelValue_105"/>
    <SBMLMap SBMLid="kkpnet_p" COPASIkey="ModelValue_106"/>
    <SBMLMap SBMLid="kkpnet_p_p" COPASIkey="ModelValue_107"/>
    <SBMLMap SBMLid="kppc1" COPASIkey="ModelValue_108"/>
    <SBMLMap SBMLid="kppf6" COPASIkey="ModelValue_109"/>
    <SBMLMap SBMLid="kppnet_p" COPASIkey="ModelValue_110"/>
    <SBMLMap SBMLid="kppnet_p_p" COPASIkey="ModelValue_111"/>
    <SBMLMap SBMLid="ks14" COPASIkey="ModelValue_112"/>
    <SBMLMap SBMLid="ks1pds_p_p" COPASIkey="ModelValue_113"/>
    <SBMLMap SBMLid="ks20_p" COPASIkey="ModelValue_114"/>
    <SBMLMap SBMLid="ks20_p_p" COPASIkey="ModelValue_115"/>
    <SBMLMap SBMLid="ks2pds_p_p" COPASIkey="ModelValue_116"/>
    <SBMLMap SBMLid="ksb2_p" COPASIkey="ModelValue_117"/>
    <SBMLMap SBMLid="ksb2_p_p" COPASIkey="ModelValue_118"/>
    <SBMLMap SBMLid="ksb5_p" COPASIkey="ModelValue_119"/>
    <SBMLMap SBMLid="ksb5_p_p" COPASIkey="ModelValue_120"/>
    <SBMLMap SBMLid="ksbud" COPASIkey="ModelValue_121"/>
    <SBMLMap SBMLid="ksc1_p" COPASIkey="ModelValue_122"/>
    <SBMLMap SBMLid="ksc1_p_p" COPASIkey="ModelValue_123"/>
    <SBMLMap SBMLid="kscdh" COPASIkey="ModelValue_124"/>
    <SBMLMap SBMLid="ksf6_p" COPASIkey="ModelValue_125"/>
    <SBMLMap SBMLid="ksf6_p_p" COPASIkey="ModelValue_126"/>
    <SBMLMap SBMLid="ksf6_p_p_p" COPASIkey="ModelValue_127"/>
    <SBMLMap SBMLid="ksn2_p" COPASIkey="ModelValue_128"/>
    <SBMLMap SBMLid="ksn2_p_p" COPASIkey="ModelValue_129"/>
    <SBMLMap SBMLid="ksnet" COPASIkey="ModelValue_130"/>
    <SBMLMap SBMLid="ksori" COPASIkey="ModelValue_131"/>
    <SBMLMap SBMLid="kspds_p" COPASIkey="ModelValue_132"/>
    <SBMLMap SBMLid="ksppx" COPASIkey="ModelValue_133"/>
    <SBMLMap SBMLid="ksspn" COPASIkey="ModelValue_134"/>
    <SBMLMap SBMLid="ksswi_p" COPASIkey="ModelValue_135"/>
    <SBMLMap SBMLid="ksswi_p_p" COPASIkey="ModelValue_136"/>
    <SBMLMap SBMLid="lte1h" COPASIkey="ModelValue_137"/>
    <SBMLMap SBMLid="lte1l" COPASIkey="ModelValue_138"/>
    <SBMLMap SBMLid="mad2h" COPASIkey="ModelValue_139"/>
    <SBMLMap SBMLid="mad2l" COPASIkey="ModelValue_140"/>
    <SBMLMap SBMLid="mdt" COPASIkey="ModelValue_141"/>
    <SBMLMap SBMLid="mu" COPASIkey="ModelValue_144"/>
    <SBMLMap SBMLid="parameter_1" COPASIkey="ModelValue_163"/>
  </SBMLReference>
</COPASI>
