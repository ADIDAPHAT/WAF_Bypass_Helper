# WAF BYPASS Helper v 0.9
    The helper has two modes of operation:
    ##Easy mode:
    It shows all variants of known bypass for your attack. Without mutation algorithm and request test
        usage: python main.py -s 'your string' -t type_of_attack --easy    

    ##Normal mode:
    Works on the following algorithm:
        1) Using universal bypass
        2) Using the results of the previous step, uses the specified bypass and tests it on the target server
        3) Print all result bypass this response status 20*,30* or 50*
    usage post: python main.py -t type_of_attack -u "url" --cookie "cookie_if_it_need" --post "csrf-token=&blog_entry=123" -s "your_atack_string" -p "param_to_inject" -o xss --proxy
    usage get: python main.py -t pathtr -u "atacked_server_url?param1=1&param2=2" -s "/etc/passwd" -p param1


# Explanations to the parameters used:

## --cookie "cookie_if_it_need"
    All cookies which must be sent
    Example: --cookie="neowize_user={2id2:24eeb5bf2-24ac-4912-a67b-99c067e645612C2version2:1.2}; PHPSESSID=6v3ecj1ffqislv49q1vfrjo2t5; showhints"

## -p "param_to_inject"
    All param which we want to inject. From 1 to ....
    If we set more than 1 param_to_inject, script test bypass in all param simultaneously
    Example:
         -p param1,param2
         -p param1;param2
         -p param1|param2

## --post "full_post_string"
    Example: --post "csrf-token=&blog_entry=123&add-to-your-blog-php-submit-button=Save+Blog+Entry"

## --proxy 
    If this param set, script use proxy settings from /main_modules/settings.py
    Standart proxy: 127.0.0.1 8080 (test on burp)

## -o file_to_output
    If you select output to a file, two files will be created:
    file_to_output         ----  A file containing only the found mutations
    file_to_output.fool    ----  A file containing the order of creating these mutations

# Type of attack

    ## sqli
    ## xss
    ## ldapi
    ## pathtr
