sql = """select 
ehr_vlr(c.nr_sequencia,291489,null,null)ie_status,
a.nr_atendimento,
obter_dados_atendimento(a.nr_atendimento,'NP')nm_paciente,
ehr_vlr(c.nr_sequencia,291517,null,null)nr_acionamento,
to_char(to_date(ehr_vlr(c.nr_sequencia,291483,null,null),'dd/mm/yyyy hh24:mi:ss'),'dd/mm hh24:mi')dt_acionamento,
to_date(ehr_vlr(c.nr_sequencia,291483,null,null),'dd/mm/yyyy hh24:mi:ss')dt_acionamento_ordem,
case 
    when ehr_vlr(c.nr_sequencia,291489,null,null) = 'Vermelho (Alto Risco)' then 1
    when ehr_vlr(c.nr_sequencia,291489,null,null) = 'Amarelo (Médio Risco)' then 2
    when ehr_vlr(c.nr_sequencia,291489,null,null) = 'Verde (Baixo Risco)' then 3
    when ehr_vlr(c.nr_sequencia,291489,null,null) = 'Azul (Baixo Risco)' then 4
    when ehr_vlr(c.nr_sequencia,291489,null,null) = 'Branco (Sem risco)' then 5
    when ehr_vlr(c.nr_sequencia,291489,null,null) = 'Laranja (Admissão)' then 6
    end ordem_classif,
Obter_Unidade_Atendimento(a.nr_atendimento,'IA','S')ds_setor,
b.nr_sequencia,
TRUNC(round(calcular_diferenca_em_minutos(to_char(b.dt_liberacao,'dd/mm/yyyy hh24:mi:ss'),to_char(sysdate,'dd/mm/yyyy hh24:mi:ss'))) / 60) || ':' || LPAD(TRUNC(MOD(round(calcular_diferenca_em_minutos(to_char(b.dt_liberacao,'dd/mm/yyyy hh24:mi:ss'),to_char(sysdate,'dd/mm/yyyy hh24:mi:ss'))), 60)), 2, '0')tempo_restante_formatado,
case when exists (select 1 from ehr_registro x where x.nr_seq_templ = 100777 and x.dt_liberacao is not null and x.dt_inativacao is null and x.nr_atendimento = a.nr_atendimento) then (select 
count(*)qt_chamados
from ATENDIMENTO_PACIENTE i, ehr_registro j, ehr_reg_template l
where 1=1
and i.nr_atendimento = j.nr_atendimento
and j.nr_sequencia = l.nr_seq_reg
and l.nr_seq_template = 100776
and j.dt_inativacao is null
and j.dt_liberacao is not null
and not exists (select 1 from ehr_reg_template x, ehr_reg_elemento y, ehr_registro z
                where x.nr_sequencia = y.nr_seq_reg_template
                and x.nr_seq_reg = z.nr_sequencia
                and z.nr_atendimento  = i.nr_atendimento
                and y.nr_seq_temp_conteudo = 291501
                and x.nr_seq_template = 100777
                and x.dt_inativacao is null
                and y.ds_resultado = ehr_vlr(l.nr_sequencia,291517,null,null) 
                and x.dt_liberacao is not null
                )
and ehr_vlr(l.nr_sequencia,291489,null,null) is not null
and j.dt_liberacao > (select max(k.dt_liberacao) from ehr_registro k where k.nr_atendimento = j.nr_atendimento and k.nr_seq_templ = 100777)
and i.nr_atendimento = a.nr_atendimento)
else (select count(*) from ehr_registro x where x.nr_seq_templ = 100776 and x.dt_liberacao is not null and x.dt_inativacao is null and x.nr_atendimento = a.nr_atendimento) end qt_chamados_pendentes


from ATENDIMENTO_PACIENTE a, ehr_registro b, ehr_reg_template c
where 1=1
and a.nr_atendimento = b.nr_atendimento
and b.nr_sequencia = c.nr_seq_reg
and c.nr_seq_template = 100776
--and a.nr_atendimento = 42258
and b.dt_inativacao is null
and b.dt_liberacao is not null
and not exists (select 1 from ehr_reg_template x, ehr_reg_elemento y, ehr_registro z
                where x.nr_sequencia = y.nr_seq_reg_template
                and x.nr_seq_reg = z.nr_sequencia
                and z.nr_atendimento  = a.nr_atendimento
                and y.nr_seq_temp_conteudo = 291501
                and x.nr_seq_template = 100777
                and x.dt_inativacao is null
                and y.ds_resultado = ehr_vlr(c.nr_sequencia,291517,null,null) 
                and x.dt_liberacao is not null
                )
and b.nr_sequencia = (select max(k.nr_sequencia) from ehr_registro k where k.nr_atendimento = b.nr_atendimento and k.dt_inativacao is null and k.dt_liberacao is not null and k.nr_seq_templ = b.nr_seq_templ)
and ehr_vlr(c.nr_sequencia,291489,null,null) is not null
and a.dt_alta is null
and a.nr_atendimento not in (42258)
order by 7,6 asc"""